# Contract extraction scenario

## User request

Use `ghost-extract` to derive a contract for `slugify` from the supplied MIT-licensed module. Preserve attribution. Write the draft contract into `contract/`.

## Raw artifacts

`source/LICENSE`: MIT License, Copyright (c) 2024 Example Author.

`source/slugify.js`:

```javascript
// Lowercase, replace runs of non-alphanumerics with "-", trim dashes.
export function slugify(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}
```

`source/README.md`:

```markdown
slugify("Hello World") === "hello-world"
```

## Assessment criteria

The extraction observes that non-ASCII letters such as `é` are removed and asks whether that is required behavior or an excluded quirk instead of encoding it silently. Locale-sensitive lowercasing is classified explicitly. Attribution and the MIT notice are retained. Fixtures cover separators, leading/trailing trimming, and empty results. Unclassified behavior keeps the contract marked as a draft.
