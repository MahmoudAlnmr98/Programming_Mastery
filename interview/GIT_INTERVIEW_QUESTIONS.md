# Git & GitHub Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Git? Explain its key features.

**Answer:**
Git is a distributed version control system.

**Key Features:**
- **Distributed**: Every developer has full repository
- **Branching**: Easy branch creation and merging
- **Speed**: Fast operations
- **Data Integrity**: SHA-1 hashing ensures data integrity
- **Free and Open Source**

### 2. Explain the difference between Git and GitHub.

**Answer:**
- **Git**: Version control system (tool)
- **GitHub**: Cloud-based hosting service for Git repositories

**Git** can be used locally without GitHub, but GitHub provides:
- Remote repository hosting
- Collaboration features
- Pull requests
- Issue tracking
- CI/CD integration

### 3. Explain basic Git commands.

**Answer:**
```bash
# Initialize repository
git init

# Clone repository
git clone <url>

# Check status
git status

# Add files
git add <file>
git add .  # All files

# Commit
git commit -m "Commit message"

# View history
git log
git log --oneline

# View changes
git diff
```

### 4. Explain Git workflow (add, commit, push).

**Answer:**
**Basic Workflow:**
```bash
# 1. Make changes to files
# 2. Stage changes
git add file.txt

# 3. Commit changes
git commit -m "Add new feature"

# 4. Push to remote
git push origin main
```

**Three Areas:**
- **Working Directory**: Files you're editing
- **Staging Area**: Files ready to commit
- **Repository**: Committed changes

### 5. Explain Git branches.

**Answer:**
Branches allow parallel development.

```bash
# Create branch
git branch feature-branch

# Switch branch
git checkout feature-branch
# Or (newer)
git switch feature-branch

# Create and switch
git checkout -b feature-branch

# List branches
git branch

# Delete branch
git branch -d feature-branch
```

### 6. Explain Git merge.

**Answer:**
Merge combines branches.

```bash
# Merge branch into current branch
git merge feature-branch

# Fast-forward merge (linear history)
# Three-way merge (creates merge commit)
```

**Merge Types:**
- **Fast-forward**: No merge commit needed
- **Three-way**: Creates merge commit
- **Squash**: Combines commits into one

### 7. Explain Git remote repositories.

**Answer:**
Remote repositories are versions of project hosted elsewhere.

```bash
# Add remote
git remote add origin <url>

# View remotes
git remote -v

# Fetch from remote
git fetch origin

# Pull (fetch + merge)
git pull origin main

# Push to remote
git push origin main
```

### 8. Explain .gitignore file.

**Answer:**
.gitignore specifies files Git should ignore.

```gitignore
# Dependencies
node_modules/
vendor/

# Build outputs
dist/
build/
*.class

# Environment files
.env
.env.local

# IDE files
.idea/
.vscode/
*.swp

# OS files
.DS_Store
Thumbs.db
```

---

## Intermediate Level

### 9. Explain Git rebase vs merge.

**Answer:**
**Merge:**
- Creates merge commit
- Preserves branch history
- Non-destructive

**Rebase:**
- Replays commits on top of base
- Linear history
- Rewrites history

```bash
# Merge
git merge feature-branch

# Rebase
git rebase main
```

**When to use:**
- **Merge**: Public branches, shared history
- **Rebase**: Local branches, clean history

### 10. Explain Git stash.

**Answer:**
Stash temporarily saves uncommitted changes.

```bash
# Stash changes
git stash
git stash save "Work in progress"

# List stashes
git stash list

# Apply stash
git stash apply
git stash pop  # Apply and remove

# Apply specific stash
git stash apply stash@{0}

# Drop stash
git stash drop stash@{0}
```

### 11. Explain Git cherry-pick.

**Answer:**
Cherry-pick applies specific commit to current branch.

```bash
# Cherry-pick commit
git cherry-pick <commit-hash>

# Cherry-pick range
git cherry-pick <start>..<end>

# Cherry-pick with no commit
git cherry-pick -n <commit-hash>
```

### 12. Explain Git reset vs revert.

**Answer:**
**Reset:**
- Moves HEAD pointer
- Can lose commits
- Use for local changes

```bash
# Soft reset (keeps changes staged)
git reset --soft HEAD~1

# Mixed reset (keeps changes unstaged)
git reset HEAD~1

# Hard reset (discards changes)
git reset --hard HEAD~1
```

**Revert:**
- Creates new commit undoing changes
- Safe for shared branches
- Preserves history

```bash
git revert <commit-hash>
```

### 13. Explain Git tags.

**Answer:**
Tags mark specific points in history (releases).

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# List tags
git tag

# Push tags
git push origin v1.0.0
git push --tags  # All tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### 14. Explain Git hooks.

**Answer:**
Hooks are scripts that run at specific Git events.

**Pre-commit Hook:**
```bash
#!/bin/sh
# .git/hooks/pre-commit
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed"
    exit 1
fi
```

**Common Hooks:**
- `pre-commit`: Before commit
- `post-commit`: After commit
- `pre-push`: Before push
- `commit-msg`: Validate commit message

### 15. Explain Git submodules.

**Answer:**
Submodules allow including one repository in another.

```bash
# Add submodule
git submodule add <repository-url> <path>

# Clone repository with submodules
git clone --recursive <repository-url>

# Update submodules
git submodule update --init --recursive
```

---

## Advanced Level

### 16. Explain Git bisect.

**Answer:**
Bisect helps find commit that introduced bug.

```bash
# Start bisect
git bisect start

# Mark bad commit
git bisect bad

# Mark good commit
git bisect good <commit-hash>

# Git checks out middle commit
# Test and mark good or bad
git bisect good
# or
git bisect bad

# Continue until bug is found
# Reset when done
git bisect reset
```

### 17. Explain Git reflog.

**Answer:**
Reflog records all HEAD movements.

```bash
# View reflog
git reflog

# Recover lost commit
git reflog
# Find commit hash
git checkout <commit-hash>
git branch recovery-branch
```

### 18. Explain Git worktree.

**Answer:**
Worktree allows multiple working directories for same repository.

```bash
# Create worktree
git worktree add ../project-feature feature-branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-feature
```

### 19. Explain Git hooks with examples.

**Answer:**
**Pre-commit Hook (Linting):**
```bash
#!/bin/sh
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed"
    exit 1
fi
```

**Commit-msg Hook (Conventional Commits):**
```bash
#!/bin/sh
commit_msg=$(cat $1)
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
    echo "Invalid commit message format"
    exit 1
fi
```

### 20. Explain GitHub workflows and CI/CD.

**Answer:**
**GitHub Actions:**
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
```

### 21. Explain Git merge strategies.

**Answer:**
**Fast-forward:**
```bash
git merge --ff-only feature-branch
```

**No-fast-forward:**
```bash
git merge --no-ff feature-branch
```

**Squash:**
```bash
git merge --squash feature-branch
git commit -m "Squashed feature"
```

### 22. Explain Git blame and annotate.

**Answer:**
Blame shows who last modified each line.

```bash
# View blame
git blame file.txt

# Blame specific lines
git blame -L 10,20 file.txt

# Ignore whitespace
git blame -w file.txt
```

### 23. Explain Git hooks automation.

**Answer:**
**Husky (Node.js):**
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm test",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  }
}
```

### 24. Explain Git LFS (Large File Storage).

**Answer:**
Git LFS handles large files.

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"

# Add .gitattributes
git add .gitattributes
```

### 25. Explain GitHub best practices.

**Answer:**
**Branching Strategy:**
- `main`: Production code
- `develop`: Development branch
- `feature/*`: Feature branches
- `hotfix/*`: Hotfix branches

**Commit Messages:**
- Use conventional commits
- Be descriptive
- Reference issues

**Pull Requests:**
- Clear description
- Link to issues
- Request reviews
- Pass CI checks

**Security:**
- Don't commit secrets
- Use .gitignore
- Review PRs carefully
- Use branch protection

---

This covers Git and GitHub interview questions from beginner to advanced level with detailed explanations and examples.

