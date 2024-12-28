import { configureStore, combineReducers } from "redux";
import { tabReducer } from 'redux';

const rootReducer = combineReducers({
    tab : tabReducer
});


export const store = configureStore({ reducer: rootReducer });