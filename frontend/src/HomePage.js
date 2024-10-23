import React, { useContext } from "react";
import { Link } from "react-router-dom";

import {doGet, useData, useCData} from "./Network";
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
        <h3>Your Saved Views</h3>
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
      <tr>
      <th>
        {toggleLink}
        {appVerboseName}
      </th>
      </tr>
      {toggled && (
        <section key={appVerboseName}>
          {models.map((modelEntry) => {
            return (
                <p key={modelEntry.verboseName} className="AppModels">

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
                    </p>
            );
          })}
        </section>
      )}
    </>
  );
}

function PendingDownloads() {
  const config = useContext(Config);
  const [downloads, loading, error] = useCData(config.downloadsUrl);

  if (!downloads) return "";

  const icons = {
    completed: (downloadUrl) => (
      <a href={downloadUrl} className="download-link" title="Download">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 16L7 11H17L12 16Z" fill="#4CAF50"/>
          <path d="M12 2V11M12 16L7 11H17L12 16ZM7 20H17" stroke="#4CAF50" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </a>
    ),
    processing: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" title="Processing">
        <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.07 4.93L16.24 7.76M19.07 19.07L16.24 16.24M4.93 19.07L7.76 16.24M4.93 4.93L7.76 7.76" stroke="#FFA500" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <animateTransform
            attributeName="transform"
            type="rotate"
            from="0 12 12"
            to="360 12 12"
            dur="5s"
            repeatCount="indefinite"
          />
        </path>
      </svg>
    ),
    error: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" title="Failed">
        <path d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#FF0000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    )
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="PendingDownloads">
      <h3 id="#AvailableDownloads">Available Downloads</h3>
      <br/>
      <table className="rightTable">
        <thead>
          <tr>
            <th>S/N</th>
            <th>Name</th>
            <th></th>
            <th>Type</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {downloads.map((download) => (
            <tr key={download.id}>
              <td>{download.id}</td>
              <td>{download.name}</td>
              <td>
                {download.status === 'completed' && icons.completed(download.downloadUrl)}
                {download.status === 'pending' && icons.processing}
                {download.status === 'error' && icons.error}
              </td>
              <td>{download.media}</td>
              <td>{formatDate(download.started)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ModelList(props) {
  const config = useContext(Config);
  return (
      <div className=" module">
          <h2>Models</h2>
          <table className="fullTable">
              {config.modelIndex.map(({appVerboseName, models}) => (
                  <AppEntry key={appVerboseName} {...{appVerboseName, models}} />
              ))}
          </table>
      </div>
  );
}


function HomePage(props) {
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  setCurrentSavedView(null);

  return (
    <div className="HomePage">
      <div className="LeftColumn">
        <ModelList />
      </div>
      <div className="RightColumn">
        <SavedAndSharedViews />
        <PendingDownloads />

      </div>
    </div>
  );
}


export { HomePage };
