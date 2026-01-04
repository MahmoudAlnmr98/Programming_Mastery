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

### 26. Explain Git hooks and their usage.

**Answer:**
Git hooks are scripts that run automatically at certain points.

**Client-Side Hooks:**
```bash
# pre-commit - Before commit
#!/bin/sh
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed"
    exit 1
fi

# commit-msg - Validate commit message
#!/bin/sh
commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "Invalid commit message format"
    exit 1
fi

# pre-push - Before push
#!/bin/sh
npm run build
```

**Server-Side Hooks:**
```bash
# pre-receive - Before accepting pushes
#!/bin/sh
while read oldrev newrev refname; do
    # Validate refs
done

# update - Before updating ref
#!/bin/sh
refname=$1
oldrev=$2
newrev=$3
# Validate specific ref
```

**Installing Hooks:**
```bash
# Manual
chmod +x .git/hooks/pre-commit
cp pre-commit .git/hooks/

# Using husky (Node.js)
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm test"
```

### 27. Explain Git workflows (GitFlow, GitHub Flow, GitLab Flow).

**Answer:**
**GitFlow:**
```
main (production)
  └── develop (development)
       ├── feature/user-auth
       ├── feature/payment
       └── release/v1.0.0
            └── hotfix/critical-bug
```

**GitHub Flow:**
```
main (always deployable)
  └── feature-branch
       (create PR → merge → deploy)
```

**GitLab Flow:**
```
main
  └── staging
       └── production
            └── feature-branch
```

**Comparison:**
- **GitFlow**: Complex, good for releases
- **GitHub Flow**: Simple, continuous deployment
- **GitLab Flow**: Environment-based

### 28. Explain Git submodules and subtrees.

**Answer:**
**Submodules:**
```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Clone with submodules
git clone --recursive https://github.com/user/main-repo.git

# Update submodules
git submodule update --remote

# Remove submodule
git submodule deinit path/to/submodule
git rm path/to/submodule
```

**Subtrees:**
```bash
# Add subtree
git subtree add --prefix=lib/repo https://github.com/user/repo.git main --squash

# Pull changes
git subtree pull --prefix=lib/repo https://github.com/user/repo.git main --squash

# Push changes
git subtree push --prefix=lib/repo https://github.com/user/repo.git main
```

**When to use:**
- **Submodules**: External dependencies, separate versioning
- **Subtrees**: Simpler, single repository

### 29. Explain Git bisect for debugging.

**Answer:**
Git bisect helps find the commit that introduced a bug.

**Usage:**
```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good <commit-hash>

# Git checks out middle commit
# Test and mark
git bisect good  # or git bisect bad

# Continue until found
git bisect reset  # When done
```

**Automated:**
```bash
git bisect start HEAD <good-commit>
git bisect run npm test
```

**Example:**
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Test each commit
git bisect good  # or bad
# Repeat until found
git bisect reset
```

### 30. Explain Git reflog and recovery.

**Answer:**
Reflog records all HEAD movements.

**View Reflog:**
```bash
git reflog
# Shows: commit-hash HEAD@{n}: action: message

git reflog show HEAD@{5}
git reflog show branch-name@{2}
```

**Recovery:**
```bash
# Recover deleted branch
git reflog
git checkout -b recovered-branch <commit-hash>

# Recover lost commit
git reflog
git cherry-pick <commit-hash>

# Reset to previous state
git reset --hard HEAD@{5}
```

**Expiration:**
```bash
# Default: 90 days
git config gc.reflogExpire "90 days"

# Keep forever
git config gc.reflogExpire "never"
```

**Use Cases:**
- Recover deleted branches
- Find lost commits
- Undo operations
- Debug issues

### 31. Explain Git Worktree.

**Answer:**
Worktree allows multiple working directories for same repository.

**Create Worktree:**
```bash
git worktree add ../feature-branch feature-branch
```

**List Worktrees:**
```bash
git worktree list
```

**Remove Worktree:**
```bash
git worktree remove ../feature-branch
```

**Use Cases:**
- Work on multiple branches simultaneously
- Testing different versions
- Parallel development

### 32. Explain Git Submodules.

**Answer:**
Submodules allow including one repository in another.

**Add Submodule:**
```bash
git submodule add https://github.com/user/repo.git path/to/submodule
```

**Clone with Submodules:**
```bash
git clone --recursive https://github.com/user/main-repo.git
# Or
git submodule update --init --recursive
```

**Update Submodule: Latest Commit:**
```bash
cd path/to/submodule
git pull origin main
cd ..
git add path/to/submodule
git commit -m "Update submodule"
```

### 33. Explain Git Hooks.

**Answer:**
Hooks are scripts that run automatically at certain points.

**Pre-commit Hook:**
```bash
#!/bin/sh
# .git/hooks/pre-commit
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed"
    exit 1
fi
```

**Pre-push Hook:**
```bash
#!/bin/sh
# .git/hooks/pre-push
npm run test
```

**Client-Side Hooks:**
- `pre-commit`: Before commit
- `prepare-commit-msg`: Before commit message editor
- `commit-msg`: Validate commit message
- `post-commit`: After commit
- `pre-push`: Before push

**Server-Side Hooks:**
- `pre-receive`: Before accepting push
- `update`: Before updating branch
- `post-receive`: After accepting push

### 34. Explain Git Bisect.

**Answer:**
Bisect helps find commit that introduced bug.

**Start Bisect:**
```bash
git bisect start
git bisect bad  # Current commit is bad
git bisect good <commit-hash>  # Known good commit
```

**Mark Current State:**
```bash
git bisect good  # Current commit is good
# Or
git bisect bad   # Current commit is bad
```

**Reset:**
```bash
git bisect reset
```

**Automated:**
```bash
git bisect run npm test
```

### 35. Explain Git Reflog.

**Answer:**
Reflog records all HEAD movements.

**View Reflog:**
```bash
git reflog
```

**Recover Lost Commit:**
```bash
git reflog
# Find commit hash
git checkout <commit-hash>
```

**Branch Reflog:**
```bash
git reflog show branch-name
```

**Use Cases:**
- Recover lost commits
- Undo operations
- Debug issues

### 36. Explain Git Cherry-pick.

**Answer:**
Cherry-pick applies specific commit to current branch.

**Basic:**
```bash
git cherry-pick <commit-hash>
```

**Multiple Commits:**
```bash
git cherry-pick <commit1> <commit2>
```

**Range:**
```bash
git cherry-pick <start-commit>..<end-commit>
```

**Edit Commit Message:**
```bash
git cherry-pick -e <commit-hash>
```

**Use Cases:**
- Apply bug fix to multiple branches
- Backport features
- Selective commit application

### 37. Explain Git Archive.

**Answer:**
Archive creates snapshot of repository.

**Create Archive:**
```bash
git archive --format=zip --output=archive.zip HEAD
```

**Specific Directory:**
```bash
git archive --format=tar --prefix=project/ HEAD | gzip > project.tar.gz
```

**Specific Branch:**
```bash
git archive --format=zip --output=archive.zip branch-name
```

**Use Cases:**
- Create releases
- Export code
- Backup snapshots

### 38. Explain Git Blame.

**Answer:**
Blame shows who last modified each line.

**Basic:**
```bash
git blame file.txt
```

**Ignore Whitespace:**
```bash
git blame -w file.txt
```

**Show Email:**
```bash
git blame -e file.txt
```

**Range:**
```bash
git blame -L 10,20 file.txt
```

**Use Cases:**
- Find author of code
- Debug issues
- Code review

### 39. Explain Git Describe.

**Answer:**
Describe finds most recent tag.

**Basic:**
```bash
git describe
# v1.0.0-5-gabc1234
```

**Always Show Tag:**
```bash
git describe --always
```

**Tags Only:**
```bash
git describe --tags
```

**Use Cases:**
- Version identification
- Build numbers
- Release tracking

### 40. Explain Git Clean.

**Answer:**
Clean removes untracked files.

**Dry Run:**
```bash
git clean -n
```

**Remove Files:**
```bash
git clean -f
```

**Remove Directories:**
```bash
git clean -fd
```

**Interactive:**
```bash
git clean -i
```

**Exclude Patterns:**
```bash
git clean -f -e "*.log"
```

### 41. Explain Git Stash Advanced Usage.

**Answer:**
**Stash with Message:**
```bash
git stash save "WIP: feature implementation"
```

**Stash Untracked Files:**
```bash
git stash -u
```

**Stash All (Including Ignored):**
```bash
git stash -a
```

**Stash Specific Files:**
```bash
git stash push -m "message" file1.txt file2.txt
```

**List Stashes:**
```bash
git stash list
```

**Show Stash:**
```bash
git stash show stash@{0}
git stash show -p stash@{0}  # With diff
```

**Apply Stash:**
```bash
git stash apply stash@{0}
git stash pop  # Apply and remove
```

**Drop Stash:**
```bash
git stash drop stash@{0}
git stash clear  # Remove all
```

### 42. Explain Git Subtree.

**Answer:**
Subtree allows including repository as subdirectory.

**Add Subtree:**
```bash
git subtree add --prefix=lib/foo https://github.com/user/foo.git main --squash
```

**Pull Updates:**
```bash
git subtree pull --prefix=lib/foo https://github.com/user/foo.git main --squash
```

**Push Changes:**
```bash
git subtree push --prefix=lib/foo https://github.com/user/foo.git main
```

**Differences from Submodules:**
- Subtree: Code included in main repo
- Submodule: Reference to external repo

### 43. Explain Git LFS (Large File Storage).

**Answer:**
LFS handles large files efficiently.

**Install:**
```bash
git lfs install
```

**Track Files:**
```bash
git lfs track "*.psd"
git lfs track "*.zip"
```

**List Tracked:**
```bash
git lfs ls-files
```

**Migrate Existing Files:**
```bash
git lfs migrate import --include="*.psd" --everything
```

**Use Cases:**
- Large binary files
- Media files
- Design assets

### 44. Explain Git Hooks with Husky.

**Answer:**
Husky makes Git hooks easy.

**Install:**
```bash
npm install --save-dev husky
npx husky install
```

**Add Hook:**
```bash
npx husky add .husky/pre-commit "npm test"
```

**Pre-commit Hook:**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm run test
```

**Commit-msg Hook:**
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx commitlint --edit $1
```

### 45. Explain Git Flow Workflow.

**Answer:**
Git Flow is branching model for releases.

**Branches:**
- `main`: Production code
- `develop`: Development branch
- `feature/*`: Feature branches
- `release/*`: Release preparation
- `hotfix/*`: Production fixes

**Commands:**
```bash
git flow init
git flow feature start new-feature
git flow feature finish new-feature
git flow release start 1.0.0
git flow release finish 1.0.0
git flow hotfix start 1.0.1
```

**Benefits:**
- Clear branching strategy
- Release management
- Hotfix handling

---

This covers Git and GitHub interview questions from beginner to advanced level with detailed explanations and examples.

