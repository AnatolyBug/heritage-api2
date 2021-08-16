import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";
import { reducer as toastrReducer } from "react-redux-toastr";
import auth from './auth';

export default (history) => combineReducers({
  router: connectRouter(history),
  auth,
  toastr: toastrReducer,
});
