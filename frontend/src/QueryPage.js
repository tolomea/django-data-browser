import * as Sentry from "@sentry/browser";
import React, { useState, useEffect, useContext } from "react";
import { useParams, useLocation } from "react-router-dom";

import { doGet, fetchInProgress } from "./Network";
import { SLink, Save, Update, useToggle, matchPrepare } from "./Util";
import { Results } from "./Results";
import { getPartsForQuery, Query, getUrlForQuery, empty } from "./Query";
import { ShowTooltip, HideTooltip } from "./Tooltip";
import { GetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";
import { FieldList } from "./FieldList";
import { FilterList } from "./FilterList";

import "./App.scss";

const BOOTING = "Booting...";
const LOADING = "Loading...";
const ERROR = "Error";

function InvalidField(props) {
  const { query, field } = props;

  return (
    <tr className="InvalidField">
      <td>
        {" "}
        <SLink onClick={() => query.removeField(field)}>close</SLink>{" "}
        {field.pathStr}
      </td>
      <td>
        <p className="Error">{field.errorMessage}</p>
      </td>
    </tr>
  );
}

function InvalidFields(props) {
  const { query } = props;
  const invalidFields = query.invalidFields();

  if (!invalidFields.length) return "";

  return (
    <div className="InvalidFields">
      <table>
        <tbody>
          {invalidFields.map((field, index) => (
            <InvalidField {...{ query, index, field }} key={index} />
          ))}
        </tbody>
      </table>
    </div>
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
      {config.modelIndex.map(({ appVerboseName, models }) => {
        return (
          <optgroup label={appVerboseName} key={appVerboseName}>
            {models.map((modelEntry) => {
              return (
                <option key={modelEntry.fullName} value={modelEntry.fullName}>
                  {appVerboseName}.{modelEntry.verboseName}
                </option>
              );
            })}
          </optgroup>
        );
      })}
    </select>
  );
}

function FieldsFilter(props) {
  const { fieldFilter, setFieldFilter } = props;
  const showTooltip = useContext(ShowTooltip);
  const hideTooltip = useContext(HideTooltip);

  return (
    <div className="FieldsFilter">
      <input
        type="text"
        value={fieldFilter}
        onChange={(event) => {
          setFieldFilter(event.target.value);
        }}
        onMouseEnter={(e) =>
          showTooltip(e, [
            "Use ' ' to seperate search terms.",
            "Use '.' to filter inside related models.",
          ])
        }
        onMouseLeave={(e) => hideTooltip(e)}
      />
      <button
        label="X"
        onClick={(event) => {
          setFieldFilter("");
        }}
      >
        X
      </button>
    </div>
  );
}

function FilterSideBar(props) {
  const { query, model } = props;
  const [fieldsToggled, fieldsToggleLink] = useToggle(true);
  const [fieldFilter, setFieldFilter] = useState("");

  return (
    <div className="FieldsList">
      <div className="FieldsToggle">{fieldsToggleLink}</div>
      {fieldsToggled && <FieldsFilter {...{ fieldFilter, setFieldFilter }} />}
      {fieldsToggled && (
        <FieldList
          {...{ query, model }}
          filterParts={matchPrepare(fieldFilter)}
        />
      )}
    </div>
  );
}

function ResultsPane(props) {
  const { query, rows, cols, body, overlay, formatHints } = props;

  if (!query.validFields().length) return <h3>No fields selected</h3>;

  return <Results {...{ query, rows, cols, body, overlay, formatHints }} />;
}

function UpdateSavedView(props) {
  const config = useContext(Config);
  const { query } = props;
  const currentSavedView = useContext(GetCurrentSavedView);

  if (!currentSavedView) return null;

  return (
    <p>
      <Update
        name={`saved view ${currentSavedView.name || "<unamed>"}`}
        apiUrl={`${config.baseUrl}api/views/${currentSavedView.pk}/`}
        data={{ ...currentSavedView, ...getPartsForQuery(query.query) }}
        redirectUrl={`/views/${currentSavedView.pk}.html`}
      />
    </p>
  );
}

function Header(props) {
  const config = useContext(Config);
  const { query, length, model, filters, limit } = props;
  const [showPopup, setShowPopup] = useState(false);
  const [popupContent, setPopupContent] = useState('');

  const handleAsyncDownload = (media) => {
    query.sendAsyncDownloadRequest(media)
      .then((response) => {
        window.location.reload();
      })
      .catch((error) => {
        setPopupContent("Error: " + error.message);
        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 5000);
      });
  };

 return (
     <header className="QueryHeader">
       <div className="QueryHeader-group">
         <ModelSelector {...{query, model}} />
         <div className="">
           <input
               id="limit-input"
               className="QueryHeader-limit"
               type="number"
          value={limit}
          onChange={(event) => {
            const newValue = Math.min(parseInt(event.target.value), config.maxRows || 1000);
            query.setLimit(newValue);
          }}
          min="1"
          max={config.maxRows || 1000}
           />
         <span className="QueryHeader-results">
          {length} results
        </span>
         </div>

       </div>


       <div className="QueryHeader-group">
         <div className="QueryHeader-dropdown">
           <button className="QueryHeader-btn">JSON</button>
           <div className="QueryHeader-dropdown-content">
             <a href={query.getUrlForMedia("json")}>Partial JSON</a>
             <a onClick={() => handleAsyncDownload("json")}>Full JSON</a>
           </div>
         </div>
         <div className="QueryHeader-dropdown">
         <button className="QueryHeader-btn">CSV</button>
           <div className="QueryHeader-dropdown-content">
             <a href={query.getUrlForMedia("csv")}>Partial CSV</a>
             <a onClick={() => handleAsyncDownload("csv")}>Full CSV</a>
           </div>
         </div>
         {/*<a href={query.getUrlForMedia("sql")} className="QueryHeader-btn">SQL</a>*/}
         <Save
             name="View"
             apiUrl={`${config.baseUrl}api/views/`}
             data={getPartsForQuery(query.query)}
             redirectUrl={(view) => `/views/${view.pk}.html`}
             className="QueryHeader-btn"
         />
       </div>
       {showPopup && (
        <div className="popup">
          <p>{popupContent}</p>
        </div>
      )}
     </header>
 );


}

function QueryPageContent(props) {
  const {
    query,
    rows,
    cols,
    body,
    length,
    model,
    filters,
    overlay,
    formatHints,
    limit,
  } = props;

  return (
      <div className="QueryPage">
        <Header
            {...{
              query,
              length,
              model,
              filters,
              limit,
            }}
        />
        <div className="MainSpace">
          <FilterSideBar {...{ query, model }} />
        <ResultsPane {...{ query, rows, cols, body, overlay, formatHints }} />
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
        ...response,
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
        getUrlForQuery(config.baseUrl, reqState, "html"),
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
      getUrlForQuery(config.baseUrl, newState, "html"),
    );

    if (!reload) return;

    fetchResults(newState).catch(handleError);
  };

  if (status === BOOTING) return "";
  const queryObj = new Query(config, query, handleQueryChange);
  return <QueryPageContent overlay={status} query={queryObj} {...query} />;
}

export { QueryPage };
