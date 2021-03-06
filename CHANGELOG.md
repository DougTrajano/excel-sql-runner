# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing unreleased.

---

## [1.1.0] - 2021-07-27

### Changed

- Added a new UI theme for this application.

### Bug fixes

- Disabled Streamlit menu.

## [1.0.0] - 2021-07-17

### Changed

- All libs was updated to the latest version
- We changed the session state custom implementation to Streamlit built-in session state.

### Bug fixes

- Now the Clear Session button will delete session state and all .sqlite files in the current folder.

## [0.1.4] - 2021-05-02

## Changed

- The user experience has been improved with `st.form` to not run the application until the user presses the button.

## [0.1.3] - 2021-05-01

## Changed

- New log logic for all the application.
- Refactored code smells identified in Sonar Analysis.

## [0.1.2] - 2021-04-19

### Changed

- Add more dependencies in `requirements.txt`

## [0.1.1] - 2021-04-18

### Changed

- `Profiling Page` Small change in layout to display SQL-statement always.
- Improvement in inference process to dtypes in `norm_df_dtypes()`.
- Disable Streamlit menu by default.

## [0.1.0] - 2021-04-18

### Added

- Added options to **Add table, Drop table** and **Show tables** in sidebar manu.
- **Home** page will provide for you a `text_input` for you run your SQL in loaded excel files.
- In **Profiling** page you can have an overview about your data sets or a specific SQL.
- **About** page is a gently introduction for this application/project. :)

---
