import React, { useContext } from "react";
import { Link, useParams } from "react-router-dom";

import { useData, Delete, CopyText } from "./Util";
import { SetCurrentSavedView } from "./CurrentSavedView";
import { Config } from "./Config";
import { ShowTooltip, HideTooltip } from "./Tooltip";

import "./App.scss";

function SavedViewPage(props) {
  const config = useContext(Config);
  const { pk } = useParams();
  const url = `${config.baseUrl}api/views/${pk}/`;
  const [view, setView] = useData(url);
  const setCurrentSavedView = useContext(SetCurrentSavedView);
  const showTooltip = useContext(ShowTooltip);
  const hideTooltip = useContext(HideTooltip);

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
                <td colSpan="2">
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
                <td colSpan="2">
                  <textarea
                    value={view.description}
                    onChange={(event) => {
                      setView({ description: event.target.value });
                    }}
                    placeholder="enter a description"
                  />
                </td>
              </tr>

              {config.canShare && (
                <tr>
                  <th>Share:</th>
                  <td>
                    <span
                      onMouseEnter={(e) => {
                        const msg = [
                          "Share this view with other users.",
                          "If they have permissions to use it then it will",
                          "appear under your name on their DDB homepage.",
                        ];
                        if (!view.name.length)
                          msg.push(
                            <strong>To be shared a view must be named.</strong>
                          );
                        showTooltip(e, msg);
                      }}
                      onMouseLeave={(e) => hideTooltip(e)}
                    >
                      <input
                        type="checkbox"
                        checked={view.shared && view.name.length}
                        onChange={(event) => {
                          setView({ shared: event.target.checked });
                        }}
                        disabled={!view.name.length}
                      />
                    </span>
                  </td>
                </tr>
              )}

              {config.canMakePublic && (
                <>
                  <tr>
                    <th>Is Public:</th>
                    <td>
                      <span
                        onMouseEnter={(e) =>
                          showTooltip(e, [
                            "Make this view availalbe at a fixed URL without a login.",
                            "This is useful for sharing the view with people who aren't",
                            "users or with third party tools like Google Sheets.",
                          ])
                        }
                        onMouseLeave={(e) => hideTooltip(e)}
                      >
                        <input
                          type="checkbox"
                          checked={view.public}
                          onChange={(event) => {
                            setView({ public: event.target.checked });
                          }}
                        />
                      </span>
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
