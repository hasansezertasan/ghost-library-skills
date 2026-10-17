// Exercise release-please's actual Node strategy offline, without GitHub writes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const releasePlease = path.resolve(process.argv[2]);
require(releasePlease); // Initialize the package's strategy registry before deep imports.
const root = path.resolve(__dirname, '../..');
const {buildStrategy} = require(path.join(releasePlease, 'build/src/factory.js'));
const {Version} = require(path.join(releasePlease, 'build/src/version.js'));
const {TagName} = require(path.join(releasePlease, 'build/src/util/tag-name.js'));
const {parseConventionalCommits} = require(path.join(releasePlease, 'build/src/commit.js'));
const config = JSON.parse(fs.readFileSync(path.join(root, 'release-please-config.json')));
const settings = config.packages['.'];
const original = fs.readFileSync(path.join(root, 'package.json'), 'utf8');
const logger = {debug() {}, info() {}, warn() {}, error() {}, trace() {}};
require(path.join(releasePlease, 'build/src/util/logger.js')).setLogger(logger);
const github = {
  repository: {owner: 'hasansezertasan', repo: 'ghost-library-skills'},
  async getFileContentsOnBranch(file) {
    assert.equal(file, 'package.json');
    return {content: Buffer.from(original).toString('base64'), parsedContent: original, sha: 'fixture'};
  },
};

(async () => {
  const results = [];
  for (const [name, message, previous, expected] of [
    ['first-release', 'feat: add ghost library workflows', undefined, '0.1.0'],
    ['patch', 'fix: repair fixture instructions', '0.1.0', '0.1.1'],
    ['feature', 'feat: add another workflow', '0.1.0', '0.2.0'],
    ['breaking-before-one', 'feat!: change contract format', '0.1.0', '0.2.0'],
  ]) {
    const strategy = await buildStrategy({releaseType: settings['release-type'] ?? config['release-type'], github, logger, targetBranch: 'main', path: '.',
      packageName: settings['package-name'] ?? 'ghost-library-skills', initialVersion: settings['initial-version'],
      includeComponentInTag: settings['include-component-in-tag'] ?? config['include-component-in-tag'] ?? false,
      bumpMinorPreMajor: settings['bump-minor-pre-major'] ?? config['bump-minor-pre-major'], changelogPath: settings['changelog-path']});
    const latest = previous ? {tag: new TagName(Version.parse(previous)), sha: 'b'.repeat(40)} : undefined;
    const pr = await strategy.buildReleasePullRequest(parseConventionalCommits([
      {sha: 'a'.repeat(40), message, files: ['skills/ghost-init/SKILL.md']},
    ], logger), latest);
    assert.ok(pr);
    assert.equal(pr.version.toString(), expected);
    const packageUpdate = pr.updates.find(update => update.path === 'package.json');
    const updated = JSON.parse(packageUpdate.updater.updateContent(original));
    const expectedPackage = JSON.parse(original);
    expectedPackage.version = expected;
    assert.deepEqual(updated, expectedPackage); // Pi declaration and file allowlist survive.
    const lockPath = path.join(root, 'package-lock.json');
    if (fs.existsSync(lockPath)) {
      const lock = fs.readFileSync(lockPath, 'utf8');
      const lockUpdate = pr.updates.find(update => update.path === 'package-lock.json');
      const updatedLock = JSON.parse(lockUpdate.updater.updateContent(lock));
      assert.equal(updatedLock.version, expected);
      assert.equal(updatedLock.packages[''].version, expected);
      assert.deepEqual(updatedLock.packages[''].devDependencies, JSON.parse(lock).packages[''].devDependencies);
    }
    assert.ok(pr.updates.find(update => update.path === 'CHANGELOG.md'));
    results.push({name, version: expected, package_fields_preserved: true, changelog_update: true,
      lockfile_checked: fs.existsSync(lockPath)});
  }
  console.log(JSON.stringify({release_please_version: require(path.join(releasePlease, 'package.json')).version,
    config: 'release-please-config.json', success: true, cases: results}, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
