# Contributing

TODO

## Versioning

follow [Semantic Versioning](https://semver.org/) 

Given a version number MAJOR.MINOR.PATCH, increment the:

* MAJOR version when you make incompatible API changes
* MINOR version when you add functionality in a backward compatible manner
* PATCH version when you make backward compatible bug fixes

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

## Commit

follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

The commit contains the following structural elements, to communicate intent to the consumers of your library:

* **fix**: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
* **feat**: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
* **BREAKING CHANGE**: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with ```MAJOR``` in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
* types other than ```fix:``` and ```feat:``` are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends ```build:```, ```chore:```, ```ci:```, ```docs:```, ```style:```, ```refactor:```, ```perf:```, ```test:```, and others.
* footers other than ```BREAKING CHANGE: <description>``` may be provided and follow a convention similar to git trailer format.

Additional types are not mandated by the Conventional Commits specification, and have no implicit effect in Semantic Versioning (unless they include a BREAKING CHANGE). A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., feat(parser): add ability to parse arrays.

## Resource

* [How to Contribute](https://opensource.guide/how-to-contribute/)
* [About Pull Requests](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
* [GitHub Help](https://help.github.com)
