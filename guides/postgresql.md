### PostgreSQL

Naming conventions: tables are pural snake case e.g `users`, `books`, `user_books`. Columns are snake case and singular, e.g  `first_name`, `created_at`. Primary keys are named `id`. Foreign keys are  Typically named `id` are reference table in singular form plus `_id` (e.g., `user_id`, `book_id`.

Example projects that use these conventions that you can check for more details:

- [Gitlab DB Schema](https://gitlab.com/gitlab-org/gitlab)
- [Discourse](https://github.com/discourse/discourse)
- [Mastodon](https://github.com/mastodon/mastodon/blob/main/db/schema.rb)
