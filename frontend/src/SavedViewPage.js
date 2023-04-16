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
          <table>
            <tbody>
              <tr>
                <td colspan="2">
                  <input
                    type="text"
                    value={view.name}
                    onChange={(event) => {
                      setView({ name: event.target.value });
                    }}
                    className="SavedViewName"
                    placeholder="enter a name"
                  />
                </td>
              </tr>

              <tr>
                <th>Folder:</th>
                <td>
                  <input
                    type="text"
                    value={view.folder}
                    onChange={(event) => {
                      setView({ folder: event.target.value });
                    }}
                    placeholder="enter a folder name"
                  />
                </td>
              </tr>

              <tr>
                <th>Model:</th>
                <td>
                  <p>{view.model}</p>
                </td>
              </tr>

              <tr>
                <th>Fields:</th>
                <td>
                  <p>{view.fields.replace(/,/g, "\u200b,")}</p>
                </td>
              </tr>

              <tr>
                <th>Filters:</th>
                <td>
                  <p>{view.query.replace(/&/g, "\u200b&")}</p>
                </td>
              </tr>

              <tr>
                <th>Limit:</th>
                <td>
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
                <td>
                  <p>{view.createdTime}</p>
                </td>
              </tr>

              <tr>
                <td colspan="2">
                  <textarea
                    value={view.description}
                    onChange={(event) => {
                      setView({ description: event.target.value });
                    }}
                    placeholder="enter a description"
                  />
                </td>
              </tr>

              {config.canMakePublic && (
                <>
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
                  {view.public && (
                    <>
                      <tr>
                        <th>Public link:</th>
                        <td>
                          <p>
                            <CopyText text={view.publicLink} />
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <th>Google Sheets:</th>
                        <td>
                          <p>
                            <CopyText text={view.googleSheetsFormula} />
                          </p>
                        </td>
                      </tr>
                    </>
                  )}
                </>
              )}
            </tbody>
          </table>
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
