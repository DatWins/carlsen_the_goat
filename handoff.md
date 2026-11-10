# Hugo Site Setup — What To Do After Creating From This Template

This template (`carlsen_the_goat`) is set up for a Hugo site using the **hugo-scroll** theme,
deployed to GitHub Pages via GitHub Actions.

Every time you create a new repo from this template, GitHub copies the files but
**drops the theme folder**. You need to add it back manually. Here is how.

---

## Step 1 — Enable GitHub Pages

1. Go to your new repo on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment → Source", select **GitHub Actions**
4. Click **Save**

---

## Step 2 — Add the Hugo Theme

GitHub does not copy the theme when you create from a template. You must add it once.

Open a terminal (Command Prompt or Git Bash on Windows), navigate to your repo folder,
then run these four commands one at a time:

```
git submodule add https://github.com/janraasch/hugo-scroll.git themes/hugo-scroll
git add .gitmodules themes/hugo-scroll
git commit -m "Add hugo-scroll theme"
git push
```

**What each command does:**
- `git submodule add` — links the hugo-scroll theme into your repo
- `git add` — stages the two new items (the link file and the theme folder)
- `git commit` — saves a snapshot with your message
- `git push` — sends it to GitHub, which triggers the Action to build and publish your site

After the push, go to the **Actions** tab in your repo. You should see a run start.
When it goes green, your site is live.

---

## Step 3 — Update the Hero Heading

Open `content/en/_index.md` and change these two lines:

```
header_headline: "Your Title Here"
header_subheadline: "Your subtitle here."
```

This controls the big heading and description visitors see at the top of the site.

## Step 4 — Update hugo.toml (optional)

Open `hugo.toml` and update the browser tab title if you want:

```toml
title = "Your Site Name – Guess the Move"
```

The `baseURL` is already set correctly by GitHub Actions, so leave that alone.

---

## Common Errors and What They Mean

| Error | Cause | Fix |
|---|---|---|
| `module "hugo-scroll" not found` | Theme submodule missing | Do Step 2 above |
| `no Dart Sass binary found` | Workflow missing Sass step | Already fixed in this template |
| `WARN Module not compatible` | Hugo version older than theme wants | Harmless warning, ignore it |
| Pages shows Jekyll/Static HTML suggestions | Workflow never ran successfully yet | Complete Step 2, then trigger the Action |

---

## What This Template Already Has

- ✅ Hugo workflow (`.github/workflows/hugo.yml`) with Dart Sass installed
- ✅ Correct `baseURL` format for GitHub Pages
- ✅ hugo-scroll theme configured in `hugo.toml`
- ❌ Theme submodule — **you must add this every time** (Step 2 above)
