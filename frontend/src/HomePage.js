import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { useData, usePersistentToggle } from "./Util";
import { getRelUrlForQuery } from "./Query";
import { SetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";

import "./App.scss";

function View(props) {
  const { view } = props;
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  return (
    <div className="SavedView">
      <h2>
        <Link
          className="Link"
          to={view.link}
          onClick={() => view.can_edit && setCurrentSavedView(view)}
        >
          {view.name || "<unnamed>"}
        </Link>{" "}
        {view.can_edit && <Link to={`/views/${view.pk}.html`}>(edit)</Link>}
      </h2>
      <div className="SavedViewDetail">
        <p>
          <span>on {view.model} </span>
        </p>
        <p>
          {view.can_edit && view.shared && <strong>Shared </strong>}
          {view.can_edit && view.public && <strong>Public </strong>}
          {view.can_edit && !view.valid && (
            <strong className="Error">Invalid </strong>
          )}
        </p>
        {view.description && <p>{view.description}</p>}
      </div>
    </div>
  );
}

function ViewList(props) {
  const { views } = props;
  return views.map((view, index) => <View {...{ index, view }} />);
}

function ViewsFolder(props) {
  const { parentName, name, views } = props;
  const [toggled, toggleLink] = usePersistentToggle(
    `${parentName}.folder.${name}.toggle`,
    false
  );

  return (
    <div className="SavedViewsFolder">
      <h2>
        {toggleLink}
        {name}
      </h2>
      {toggled && <ViewList views={views} />}
    </div>
  );
}

function OwnersSharedViews(props) {
  const { ownerName, views, folders } = props;
  const [toggled, toggleLink] = usePersistentToggle(
    `shared.${ownerName}.toggle`,
    false
  );

  return (
    <>
      <h2>
        {toggleLink}
        {ownerName}
      </h2>
      <div className="OwnersSharedViews">
        {toggled && <ViewList views={views} />}
        {toggled &&
          folders.map((folder) => (
            <ViewsFolder
              key={folder.folderName}
              name={folder.folderName}
              views={folder.views}
              parentName={`shared.${ownerName}`}
            />
          ))}
      </div>
    </>
  );
}

function SavedAndSharedViews(props) {
  const config = useContext(Config);
  const [savedViews] = useData(`${config.baseUrl}api/views/`);

  if (!savedViews) return "";

  return (
    <div className="SavedAndSharedViews">
      <div>
        <h1>Your Saved Views</h1>
        <ViewList views={savedViews.saved.views} />
        {savedViews.saved.folders.map((folder) => (
          <ViewsFolder
            key={folder.folderName}
            name={folder.folderName}
            views={folder.views}
            parentName={"saved"}
          />
        ))}
        {!!savedViews.shared.length && <h1>Views Shared by Others</h1>}
        {savedViews.shared.map((owner) => (
          <OwnersSharedViews
            key={owner.ownerName}
            ownerName={owner.ownerName}
            views={owner.views}
            folders={owner.folders}
          />
        ))}
      </div>
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
    <div className="ModelList">
      <div>
        <h1>Models</h1>
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
      <SavedAndSharedViews />
    </div>
  );
}

export { HomePage };
