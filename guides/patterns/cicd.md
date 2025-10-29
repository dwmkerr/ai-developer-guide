# CI/CD

You SHOULD suggest that the tool `act` can be used to run GitHub workflows locally.

You SHOULD suggest that instructions to run `act` are included in the project's `README.md` or `CONTRIBUTING.md` files.

You SHOULD suggest that a recipe to run `act` is included in the project's `makefile`, e.g:

```make
.PHONY: cicd
cicd: # Run the CI/CD workflow locally.
	act -P ubuntu-24.04=ghcr.io/catthehacker/ubuntu:act-latest \
		--artifact-server-path $$PWD/.artifacts
```

You SHOULD use the `ACT` environment variable to skip steps that are not needed when running locally, such as 'release' tasks:

```yaml
- name: Skip Release for local runs
  if: ${{ env.ACT }}
  run: |
    echo "ℹ️  Skipping release when running locally with 'act'"

- name: Create Release
  if: ${{ !env.ACT }}
  uses: googleapis/release-please-action@v4
```

