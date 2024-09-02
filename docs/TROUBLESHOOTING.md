# Troubleshooting

This document provides guidance on troubleshooting common issues encountered while using GraphFleet.

## 1. API Key Errors

**Problem:** You encounter errors related to API keys, such as "Invalid API key" or "Authentication failed."

**Solution:**

- **Verify API Key:** Double-check that you have entered the correct API keys for all required services in your `.env` file.
- **Key Validity:** Ensure that your API keys are valid and have not expired.
- **Rate Limits:** Check if you have exceeded any rate limits imposed by the external services you are using.

## 2. Data Loading Issues

**Problem:** GraphFleet fails to load data from the specified input directory.

**Solution:**

- **Path Verification:** Verify that the `INPUT_DIR` setting in `app/config.py` points to the correct directory containing your data files.
- **File Format:** Ensure that your data files are in a supported format (e.g., text files, CSV files).
- **File Permissions:** Check if the application has sufficient permissions to read files from the input directory.

## 3. Search Functionality Problems

**Problem:** Searches are not returning expected results or are returning errors.

**Solution:**

- **Query Formulation:** Review your search queries and ensure they are clear and specific.
- **Data Relevance:** Check if the data loaded into GraphFleet is relevant to your search queries.
- **Index Integrity:** If you have recently updated your data, ensure that the knowledge graph index has been rebuilt.

## 4. Performance Issues

**Problem:** GraphFleet is running slowly or experiencing performance bottlenecks.

**Solution:**

- **Resource Constraints:** Check if your system has sufficient memory and CPU resources available.
- **Caching:** Enable caching mechanisms in `graphfleet/settings.yaml` to improve performance for repeated queries.
- **Data Optimization:** Consider optimizing your data by reducing its size or complexity.

## 5. Logging and Debugging

**Problem:** You need to debug an issue or gather more information about an error.

**Solution:**

- **Enable Logging:** Set the logging level to `DEBUG` in `app/main.py` to enable detailed logging.
- **Error Tracking:** GraphFleet integrates with Sentry for error tracking. Check the Sentry dashboard for error reports and stack traces.

## 6. Getting Help

If you encounter any other issues or need further assistance, please consult the GraphFleet documentation or reach out to the project maintainers for support.