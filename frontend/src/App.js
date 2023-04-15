import React, { useContext } from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import { ContextMenu } from "./ContextMenu";
import { Tooltip } from "./Tooltip";
import { CurrentSavedView } from "./CurrentSavedView";
import { HomePage } from "./HomePage";
import { QueryPage } from "./QueryPage";
import { SavedViewPage } from "./SavedViewPage";
import { version } from "./Util";
import { Config } from "./Config";

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
  const config = useContext(Config);
  return (
    <BrowserRouter basename={config.baseUrl}>
      <ContextMenu>
        <Tooltip>
          <CurrentSavedView>
            <Logo />
            <Switch>
              <Route path="/query/:model/:fieldStr?.html">
                <QueryPage />
              </Route>
              <Route path="/views/:pk.html">
                <SavedViewPage />
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
