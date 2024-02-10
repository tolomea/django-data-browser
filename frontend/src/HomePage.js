import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { useData } from "./Network";
import { usePersistentToggle } from "./Util";
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

function Folder(props) {
  const { parentName, folder, foldersExpanded } = props;
  const fullName = `${parentName}.${folder.name}`;
  const [toggled, toggleLink] = usePersistentToggle(
    `${fullName}.toggle`,
    foldersExpanded,
  );

  return (
    <div className="SavedViewsFolder">
      <h2>
        {toggleLink}
        {folder.name}
      </h2>
      {toggled && <Entries entries={folder.entries} {...{ foldersExpanded }} />}
    </div>
  );
}

function Entries(props) {
  const { entries, parentName, foldersExpanded } = props;
  return entries.map((entry, index) =>
    entry.type === "view" ? (
      <View key={index} view={entry} />
    ) : (
      <Folder key={index} folder={entry} {...{ parentName, foldersExpanded }} />
    ),
  );
}

function SavedAndSharedViews(props) {
  const config = useContext(Config);
  const [savedViews] = useData(`${config.baseUrl}api/views/`);

  if (!savedViews) return ""; // loading state

  return (
    <div className="SavedAndSharedViews">
      <div>
        <h1>Your Saved Views</h1>
        <Entries
          entries={savedViews.saved}
          parentName="saved"
          foldersExpanded={true}
        />
        {!!savedViews.shared.length && <h1>Views Shared by Others</h1>}
        <Entries
          entries={savedViews.shared}
          parentName="shared"
          foldersExpanded={false}
        />
      </div>
    </div>
  );
}

function AppEntry(props) {
  const config = useContext(Config);
  const { appVerboseName, models } = props;
  const [toggled, toggleLink] = usePersistentToggle(
    `model.${appVerboseName}.toggle`,
    config.appsExpanded,
  );
  return (
    <>
      <h2>
        {toggleLink}
        {appVerboseName}
      </h2>
      {toggled && (
        <div key={appVerboseName} className="AppModels">
          {models.map((modelEntry) => {
            return (
              <h2 key={modelEntry.verboseName}>
                <Link
                  to={getRelUrlForQuery(
                    {
                      model: modelEntry.fullName,
                      fields: [],
                      filters:
                        config.allModelFields[modelEntry.fullName]
                          .defaultFilters,
                      limit: config.defaultRowLimit,
                    },
                    "html",
                  )}
                  className="Link"
                >
                  {modelEntry.verboseName}
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
        {config.modelIndex.map(({ appVerboseName, models }) => (
          <AppEntry key={appVerboseName} {...{ appVerboseName, models }} />
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
