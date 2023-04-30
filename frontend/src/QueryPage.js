import * as Sentry from "@sentry/browser";
import React, { useState, useEffect, useContext } from "react";
import { useParams, useLocation } from "react-router-dom";

import {
  TLink,
  SLink,
  Save,
  Update,
  HasActionIcon,
  HasToManyIcon,
  useToggle,
  doGet,
  fetchInProgress,
} from "./Util";
import { Results } from "./Results";
import { getPartsForQuery, Query, getUrlForQuery, empty } from "./Query";
import { ShowTooltip, HideTooltip } from "./Tooltip";
import { GetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";

import "./App.scss";

const assert = require("assert");

const BOOTING = "Booting...";
const LOADING = "Loading...";
const ERROR = "Error";

function FilterValue(props) {
  const { lookupType, onChange, value, field } = props;
  const onChangeEvent = (e) => onChange(e.target.value);
  const showTooltip = useContext(ShowTooltip);
  const hideTooltip = useContext(HideTooltip);
  const helpText = {
    date: [
      "Date filter values consist of a series of clauses applied in order left to right starting with a value of `today`.",
      "e.g. 'day=1 month+1 tuesday+2' which means move to the 1st of this month, then move forward a month, then move forward to the second Tuesday.",
      "Possible clauses include 'today', 'now' and literal date values in a variety of formats e.g. '2020-12-21'.",
      "Or you can use 'year', 'month', 'week' or 'day' with '+', '-', or '=' to add remove or replace the given quantity.",
      "Or you can use a weekday name with '+' or '-' to get the n-th next or previous (including today) instance of that day.",
      "Bear in mind that 'day=1 month+1' may produce a different result from 'month+1 day=1', for example on Jan 31st.",
    ],
    datetime: [
      "Datetime filter consist of a series of clauses applied in order left to right starting with a value of `now`.",
      "e.g. 'day=1 month+1 tuesday+2' which means move to the 1st of this month, then move forward a month, then move forward to the second Tuesday.",
      "Possible clauses include 'today', 'now' and literal date and time values in a variety of formats e.g. '2020-12-21 14:56'.",
      "Or you can use 'year', 'month', 'week', 'day', 'hour', 'minute' or 'second' with '+', '-', or '=' to add remove or replace the given quantity.",
      "Or you can use a weekday name with '+' or '-' to get the n-th next or previous (including today) instance of that day.",
      "Bear in mind that 'day=1 month+1' may produce a different result from 'month+1 day=1', for example on Jan 31st.",
    ],
  };

  if (lookupType === "boolean") {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={true}>true</option>
        <option value={false}>false</option>
      </select>
    );
  } else if (lookupType === "isnull") {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        <option value={"IsNull"}>IsNull</option>
        <option value={"NotNull"}>NotNull</option>
      </select>
    );
  } else if (lookupType.endsWith("choice")) {
    return (
      <select {...{ value }} onChange={onChangeEvent} className="FilterValue">
        {field.choices.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    );
  } else if (lookupType === "number") {
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="number"
        step="0"
      />
    );
  } else if (lookupType === "jsonfield") {
    const parts = value.split(/\|(.*)/);
    return (
      <>
        <input
          value={parts[0]}
          onChange={(e) => onChange(`${e.target.value}|${parts[1]}`)}
          className="FilterValue Half"
          type="text"
        />
        <input
          value={parts[1]}
          onChange={(e) => onChange(`${parts[0]}|${e.target.value}`)}
          className="FilterValue Half"
          type="text"
        />
      </>
    );
  } else {
    return (
      <input
        {...{ value }}
        onChange={onChangeEvent}
        className="FilterValue"
        type="text"
        onMouseEnter={(e) => showTooltip(e, helpText[lookupType])}
        onMouseLeave={(e) => hideTooltip(e)}
      />
    );
  }
}

function Filter(props) {
  const { pathStr, index, lookup, query, value, errorMessage, parsed } = props;
  const field = query.getField(pathStr);
  var type = null;
  var lookupType = null;
  if (field !== null) {
    type = query.getType(field);
    if (type.lookups.hasOwnProperty(lookup))
      lookupType = type.lookups[lookup].type;
  }

  if (lookupType === null)
    return (
      <tr className="Filter">
        <td>
          {" "}
          <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
          {pathStr}
        </td>
        <td>{lookup}</td>
        <td>=</td>
        <td>
          {value}
          <p className="Error">{errorMessage}</p>
        </td>
      </tr>
    );

  return (
    <tr className="Filter">
      <td>
        <SLink onClick={() => query.removeFilter(index)}>close</SLink>{" "}
        <TLink onClick={() => query.addField(pathStr, field.defaultSort)}>
          {query.prettyPathStr(pathStr)}
        </TLink>{" "}
      </td>
      <td>
        <select
          className="Lookup"
          value={lookup}
          onChange={(e) => query.setFilterLookup(index, e.target.value)}
        >
          {type.sortedLookups.map((lookupName) => (
            <option key={lookupName} value={lookupName}>
              {type.lookups[lookupName].prettyName}
            </option>
          ))}
        </select>
      </td>
      <td>=</td>
      <td>
        <FilterValue
          {...{ value, field, lookupType }}
          onChange={(val) => query.setFilterValue(index, val)}
        />
        {errorMessage && <p className="Error">{errorMessage}</p>}
        {parsed !== null &&
          (lookupType === "date" || lookupType === "datetime") && (
            <p className="Success">{parsed}</p>
          )}
      </td>
    </tr>
  );
}

function Filters(props) {
  const { query, filterErrors, parsedFilterValues, filters } = props;
  const [toggled, toggleLink] = useToggle(true);
  if (!filters.length) return "";
  return (
    <form className="Filters" onSubmit={(e) => e.preventDefault()}>
      <div className="FiltersToggle">{toggleLink}</div>
      {toggled && (
        <table>
          <tbody>
            {filters.map((filter, index) => (
              <Filter
                {...{ query, index }}
                {...filter}
                key={index}
                errorMessage={filterErrors[index]}
                parsed={parsedFilterValues[index]}
              />
            ))}
          </tbody>
        </table>
      )}
    </form>
  );
}

function Field(props) {
  const { query, path, modelField } = props;
  const type = query.getType(modelField);
  const [toggled, toggleLink] = useToggle();

  return (
    <>
      <tr className="Field">
        {/* filter */}
        <td>
          {modelField.concrete && type.defaultLookup && (
            <SLink onClick={() => query.addFilter(path.join("__"))}>
              filter_alt
            </SLink>
          )}
        </td>

        {/* expand */}
        <td>{modelField.model && toggleLink}</td>

        {/* name */}
        <td className={`FieldName ${query.getFieldClass(modelField)}`}>
          {modelField.type ? (
            <TLink
              onClick={() =>
                query.addField(path.join("__"), modelField.defaultSort)
              }
            >
              {modelField.prettyName}
              <HasActionIcon
                modelField={modelField}
                message="Has admin actions."
              />
            </TLink>
          ) : (
            <>
              {modelField.prettyName}
              <HasToManyIcon
                modelField={modelField}
                message="Traversing 'To Many' links may add multiple lines per result."
              />
            </>
          )}
        </td>
      </tr>

      {/* sub fields */}
      {toggled && (
        <tr>
          <td></td>
          <td colSpan="2">
            <FieldGroup {...{ query, path }} model={modelField.model} />
          </td>
        </tr>
      )}
    </>
  );
}

function FieldGroup(props) {
  const { query, model, path } = props;
  const modelFields = query.getModelFields(model);
  return (
    <table className="FieldGroup">
      <tbody>
        {modelFields.sortedFields.map((fieldName) => {
          const modelField = modelFields.fields[fieldName];
          return (
            <Field
              key={fieldName}
              {...{ query, modelField }}
              path={path.concat([fieldName])}
            />
          );
        })}
      </tbody>
    </table>
  );
}

function ModelSelector(props) {
  const config = useContext(Config);
  const { query, model } = props;

  return (
    <select
      className="ModelSelector"
      onChange={(e) => query.setModel(e.target.value)}
      value={model}
    >
      {config.sortedModels.map(({ appName, modelNames }) => {
        return (
          <optgroup label={appName} key={appName}>
            {modelNames.map((modelName) => {
              const fullName = `${appName}.${modelName}`;
              return <option key={fullName}>{fullName}</option>;
            })}
          </optgroup>
        );
      })}
    </select>
  );
}

function QueryPageContent(props) {
  const config = useContext(Config);
  const {
    query,
    rows,
    cols,
    body,
    length,
    model,
    filters,
    filterErrors,
    parsedFilterValues,
    overlay,
    formatHints,
  } = props;

  let results;
  if (query.query.fields.length)
    results = (
      <Results {...{ query, rows, cols, body, overlay, formatHints }} />
    );
  else results = <h1>No fields selected</h1>;

  const [fieldsToggled, fieldsToggleLink] = useToggle(true);
  const currentSavedView = useContext(GetCurrentSavedView);

  var updateSavedViewLink = null;
  if (currentSavedView) {
    const savedViewName = currentSavedView.name
      ? `"${currentSavedView.name}"`
      : "<unamed>";
    updateSavedViewLink = (
      <p>
        <Update
          name={`saved view ${savedViewName}`}
          apiUrl={`${config.baseUrl}api/views/${currentSavedView.pk}/`}
          data={{ ...currentSavedView, ...getPartsForQuery(query.query) }}
          redirectUrl={`/views/${currentSavedView.pk}.html`}
        />
      </p>
    );
  }

  return (
    <div className="QueryPage">
      <ModelSelector {...{ query, model }} />
      <Filters {...{ query, filters, filterErrors, parsedFilterValues }} />
      <p>
        <span className={length >= query.query.limit ? "Error" : ""}>
          Limit:{" "}
          <input
            className="RowLimit"
            type="number"
            value={query.query.limit}
            onChange={(event) => {
              query.setLimit(event.target.value);
            }}
            min="1"
          />{" "}
          - Showing {length} results -{" "}
        </span>
        <a href={query.getUrlForMedia("csv")}>Download as CSV</a> -{" "}
        <a href={query.getUrlForMedia("json")}>View as JSON</a> -{" "}
        <a href={query.getUrlForMedia("sql")}>View SQL Query</a> -{" "}
        <Save
          name="View"
          apiUrl={`${config.baseUrl}api/views/`}
          data={getPartsForQuery(query.query)}
          redirectUrl={(view) => `/views/${view.pk}.html`}
        />
      </p>
      {updateSavedViewLink}
      <div className="MainSpace">
        <div className="FieldsList">
          <div className="FieldsToggle">{fieldsToggleLink}</div>
          {fieldsToggled && (
            <div className="Scroller">
              <FieldGroup {...{ query, model }} path={[]} />
            </div>
          )}
        </div>
        {results}
        <div />
      </div>
    </div>
  );
}

function QueryPage(props) {
  const config = useContext(Config);
  const { model, fieldStr } = useParams();
  const [status, setStatus] = useState(BOOTING);
  const [query, setQuery] = useState({
    model: "",
    fields: [],
    filters: [],
    limit: config.defaultRowLimit,
    ...empty,
  });
  const queryStr = useLocation().search;

  const handleError = (e) => {
    if (e.name !== "AbortError") {
      setStatus(ERROR);
      console.log(e);
      Sentry.captureException(e);
    }
  };

  const fetchResults = (state) => {
    setStatus(LOADING);
    const url = getUrlForQuery(config.baseUrl, state, "json");

    return doGet(url).then((response) => {
      setQuery((query) => ({
        ...query,
        body: response.body,
        cols: response.cols,
        rows: response.rows,
        length: response.length,
        formatHints: response.formatHints,
        filterErrors: response.filterErrors,
        parsedFilterValues: response.parsedFilterValues,
      }));
      setStatus(fetchInProgress ? LOADING : undefined);
      return response;
    });
  };

  useEffect(() => {
    const popstate = (e) => {
      setQuery(e.state);
      fetchResults(e.state).catch(handleError);
    };

    const url = `${config.baseUrl}query/${model}/${
      fieldStr || ""
    }.query${queryStr}`;

    doGet(url).then((response) => {
      const reqState = {
        model: response.model,
        fields: response.fields,
        filters: response.filters,
        limit: response.limit,
        ...empty,
      };
      setQuery(reqState);
      setStatus(LOADING);
      window.history.replaceState(
        reqState,
        null,
        getUrlForQuery(config.baseUrl, reqState, "html")
      );
      window.addEventListener("popstate", popstate);
      fetchResults(reqState).catch(handleError);
    });

    return () => {
      window.removeEventListener("popstate", popstate);
    };
    // eslint-disable-next-line
  }, []);

  const handleQueryChange = (queryChange, reload = true) => {
    const newState = { ...query, ...queryChange };

    setQuery(newState);

    const request = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
      limit: newState.limit,
      ...empty,
    };
    window.history.pushState(
      request,
      null,
      getUrlForQuery(config.baseUrl, newState, "html")
    );

    if (!reload) return;

    fetchResults(newState)
      .then((response) => {
        const res = { ...response, ...empty };
        const req = { ...request };
        assert.deepStrictEqual(res, req);
      })
      .catch(handleError);
  };

  if (status === BOOTING) return "";
  const queryObj = new Query(config, query, handleQueryChange);
  return <QueryPageContent overlay={status} query={queryObj} {...query} />;
}

export { QueryPage };
