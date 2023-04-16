import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { useData, usePersistentToggle } from "./Util";
import { getRelUrlForQuery } from "./Query";
import { SetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";

import "./App.scss";

function SavedViews(props) {
  const { views } = props;
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  return (
    <>
      {views.map((view, index) => (
        <div key={index} className="SavedView">
          <h2>
            <Link
              className="Link"
              to={view.link}
              onClick={() => setCurrentSavedView(view)}
            >
              {view.name || "<unnamed>"}
            </Link>
          </h2>
          <p>
            on {view.model} - <Link to={`/views/${view.pk}.html`}>edit</Link>
          </p>
          <p>{view.description}</p>
        </div>
      ))}
    </>
  );
}

function SavedViewFolder(props) {
  const { name, views } = props;
  const [toggled, toggleLink] = usePersistentToggle(
    `folder.${name}.toggle`,
    false
  );

  return (
    <div className="SavedViewFolder">
      <h2>
        {toggleLink}
        {name}
      </h2>
      {toggled && <SavedViews views={views} />}
    </div>
  );
}

function SavedViewList(props) {
  const config = useContext(Config);
  const [savedViews] = useData(`${config.baseUrl}api/views/`);

  if (!savedViews) return "";
  return (
    <div className="SavedViewList">
      <h1>Saved Views</h1>

      {savedViews.map((folder) => {
        if (folder.name !== "")
          return (
            <SavedViewFolder
              views={folder.views}
              name={folder.name}
              key={folder.name}
            />
          );
        else return <SavedViews views={folder.views} />;
      })}
    </div>
  );
}

function AppEntry(props) {
  const config = useContext(Config);
  const { appName, modelNames } = props;
  const [toggled, toggleLink] = usePersistentToggle(
    `model.${appName}.toggle`,
    config.appsExpanded
  );
  return (
    <>
      <h2>
        {toggleLink}
        {appName}
      </h2>
      {toggled && (
        <div key={appName} className="AppModels">
          {modelNames.map((modelName) => {
            const fullName = `${appName}.${modelName}`;
            return (
              <h2 key={modelName}>
                <Link
                  to={getRelUrlForQuery(
                    {
                      model: fullName,
                      fields: [],
                      filters: config.allModelFields[fullName].defaultFilters,
                      limit: config.defaultRowLimit,
                    },
                    "html"
                  )}
                  className="Link"
                >
                  {modelName}
                </Link>
              </h2>
            );
          })}
        </div>
      )}
    </>
  );
}

function ModelList(props) {
  const config = useContext(Config);
  return (
    <div>
      <h1>Models</h1>
      <div className="AppList">
        {config.sortedModels.map(({ appName, modelNames }) => (
          <AppEntry key={appName} {...{ appName, modelNames }} />
        ))}
      </div>
    </div>
  );
}

function HomePage(props) {
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  setCurrentSavedView(null);

  return (
    <div className="HomePage">
      <ModelList />
      <SavedViewList />
    </div>
  );
}

export { HomePage };
