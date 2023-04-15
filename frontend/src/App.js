import React from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import { ContextMenu } from "./ContextMenu";
import { Tooltip } from "./Tooltip";
import { CurrentSavedView } from "./CurrentSavedView";
import { HomePage } from "./HomePage";
import { QueryPage } from "./QueryPage";
import { SavedViewPage } from "./SavedViewPage";
import { version } from "./Util";

import "./App.scss";

function Logo(props) {
  return (
    <Link to="/" className="Logo">
      <span>DDB</span>
      <span className="Version">v{version}</span>
    </Link>
  );
}

function App(props) {
  const { baseUrl, canMakePublic } = props;
  return (
    <BrowserRouter basename={baseUrl}>
      <ContextMenu>
        <Tooltip>
          <CurrentSavedView>
            <Logo />
            <Switch>
              <Route path="/query/:model/:fieldStr?.html">
                <QueryPage config={props} />
              </Route>
              <Route path="/views/:pk.html">
                <SavedViewPage {...{ baseUrl, canMakePublic }} />
              </Route>
              <Route path="/">
                <HomePage />
              </Route>
            </Switch>
          </CurrentSavedView>
        </Tooltip>
      </ContextMenu>
    </BrowserRouter>
  );
}

export default App;
