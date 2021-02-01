import * as Sentry from "@sentry/browser";
import React, { useState, useEffect } from "react";
import {
  BrowserRouter,
  Switch,
  Route,
  useParams,
  useLocation,
} from "react-router-dom";
import "./App.css";
import { ContextMenu } from "./ContextMenu";
import { Tooltip } from "./Tooltip";
import { HomePage, QueryPage, Logo, EditSavedView } from "./Components";
import { Query, getUrlForQuery, empty } from "./Query";
import { doGet, fetchInProgress } from "./Util";

const assert = require("assert");

const BOOTING = "Booting...";
const LOADING = "Loading...";
const ERROR = "Error";

function QueryApp(props) {
  const { config } = props;
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
  return (
    <QueryPage
      overlay={status}
      query={queryObj}
      sortedModels={config.sortedModels}
      baseUrl={config.baseUrl}
      {...query}
    />
  );
}

function App(props) {
  const { baseUrl, canMakePublic } = props;
  return (
    <BrowserRouter basename={baseUrl}>
      <ContextMenu>
        <Tooltip>
          <Logo />
          <Switch>
            <Route path="/query/:model/:fieldStr?.html">
              <QueryApp config={props} />
            </Route>
            <Route path="/views/:pk.html">
              <EditSavedView {...{ baseUrl, canMakePublic }} />
            </Route>
            <Route path="/">
              <HomePage {...props} />
            </Route>
          </Switch>
        </Tooltip>
      </ContextMenu>
    </BrowserRouter>
  );
}

export default App;
