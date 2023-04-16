import React, { useContext } from "react";
import { Link, useParams } from "react-router-dom";

import { useData, Delete, CopyText } from "./Util";
import { SetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";

import "./App.scss";

function SavedViewPage(props) {
  const config = useContext(Config);
  const { pk } = useParams();
  const url = `${config.baseUrl}api/views/${pk}/`;
  const [view, setView] = useData(url);
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  setCurrentSavedView(null);

  if (!view) return "";
  return (
    <div className="EditSavedView">
      <div>
        <div className="SavedViewActions">
          <span className="SavedViewTitle">Saved View</span>
          <Link to={view.link} onClick={() => setCurrentSavedView(view)}>
            Open
          </Link>
        </div>
        <form>
          <input
            type="text"
            value={view.name}
            onChange={(event) => {
              setView({ name: event.target.value });
            }}
            className="SavedViewName"
            placeholder="enter a name"
          />
          <table>
            <tbody>
              <tr>
                <th>Model:</th>
                <td>{view.model}</td>
              </tr>
              <tr>
                <th>Fields:</th>
                <td>{view.fields.replace(/,/g, "\u200b,")}</td>
              </tr>
              <tr>
                <th>Filters:</th>
                <td>{view.query.replace(/&/g, "\u200b&")}</td>
              </tr>
              <tr>
                <th>Limit:</th>
                <td className="SavedViewLimit">
                  <input
                    className="RowLimit"
                    type="number"
                    value={view.limit}
                    onChange={(event) => {
                      setView({ limit: event.target.value });
                    }}
                  />
                </td>
              </tr>
              <tr>
                <th>Created Time:</th>
                <td>{view.createdTime}</td>
              </tr>
            </tbody>
          </table>
          <textarea
            value={view.description}
            onChange={(event) => {
              setView({ description: event.target.value });
            }}
            placeholder="enter a description"
          />
          {config.canMakePublic && (
            <table>
              <tbody>
                <tr>
                  <th>Is Public:</th>
                  <td>
                    <input
                      type="checkbox"
                      checked={view.public}
                      onChange={(event) => {
                        setView({ public: event.target.checked });
                      }}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Public link:</th>
                  <td>{view.public && <CopyText text={view.publicLink} />}</td>
                </tr>
                <tr>
                  <th>Google Sheets:</th>
                  <td>
                    {view.public && (
                      <CopyText text={view.googleSheetsFormula} />
                    )}
                  </td>
                </tr>
              </tbody>
            </table>
          )}
        </form>
        <div className="SavedViewActions">
          <Delete apiUrl={url} redirectUrl="/" />
          <Link to="/">Close</Link>
        </div>
      </div>
    </div>
  );
}

export { SavedViewPage };