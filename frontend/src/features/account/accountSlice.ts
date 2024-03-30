import { PayloadAction, Slice } from "@reduxjs/toolkit";
import { createAppSlice } from "../../app/createAppSlice";
import { server_base_url} from "../../appsettings.json"

// Define types for account state
export type AccountResponse = {
  user_account_id: string;
  email: string;
  username: string;
  password: string;
}

// Define initial state
export type AccountState = AccountResponse;

// Initialize an Account object with provided parameters
const initializeAccountState = (
  user_account_id: string,
  email: string,
  username: string,
  password: string,
): AccountState => {
  return {
    user_account_id: user_account_id,
    email: email,
    username: username,
    password: password,
  }
}

// Define initial state
const initialState : AccountState = {
  user_account_id: "",
  email: "",
  username: "",
  password: "",  
};

export const accountSlice: Slice = createAppSlice({
  // Define account slice
  name: "account",
  initialState,
  reducers: create => ({
    // Reducer function to set the current account
    setCurrentAccount: create.reducer(
      (state, action: PayloadAction<AccountResponse>) => {
        state.current = initializeAccountState(
          action.payload.user_account_id,
          action.payload.email,
          action.payload.username,
          action.payload.password,
        )
      },
    ),
    // Define async thunk for creating account information
    createAccount: create.asyncThunk(
    async (args: {
      email: string,
      username: string,
      password: string,
    }): 
    Promise<any> => {
      const { email, username, password } = args
      fetch(
        `${server_base_url}/create_account`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, username: username, password: password }),
        }
      ).then(response => {
        if (response.ok) {
          return response.json()
        }
        console.error("Failed to create account")
      })
    },
    {
      pending: state => {
        // do nothing
      },
      fulfilled: (state, action) => {
        if (!state.current) {
          // the user closed account creation view or response expired, do nothing
          console.warn(
            `Incoming account creation, but the session expired.`)
          console.log("Response is ignored.")
        }
      },
      rejected: state => {
        console.error("Failed to create account")
      },
    },
  ),
    
    // Define async thunk for fetching account information
    fetchAccountInfo: create.asyncThunk(
      async (): 
      Promise<any> => {
        fetch(`${server_base_url}/get_account`, {
          method: "GET",
          credentials: "same-origin", // to enable cookies so that user account id can get through
        }).then(response => {
          if (response.ok) {
            return response.json()
          }
          console.error("Failed to fetch account information")
        })
      },
      {
        pending: state => {
          // do nothing
        },
        fulfilled: (state, action) => {
          const { user_account_id, email, username, password } = action.payload
          if (state.current && state.current.user_account_id === user_account_id) {
            // response is valid
            state.current.email = email
            state.current.username = username
            state.current.password = password
          } 
          else {
            // the user closed account information view or response expired, do nothing
            console.warn(
              `Incoming account information, but the account view expired.`)
            console.log("Response is ignored.")
          }
        },
        rejected: state => {
          console.error("Failed to fetch account information")
        },
      },
    ),

    // Define async thunk for updating account 
    updateAccount: create.asyncThunk(
      async (account_info: { user_account_id: string; email: string; username: string; password: string }): 
      Promise<any> => {
        fetch(`${server_base_url}/update_account`, {
          method: "PUT",
          credentials: "same-origin", // to enable cookies so that user account id can get through
          body: JSON.stringify(account_info)
        }).then(response => {
          if (response.ok) {
            return response.json()
          }
          console.error("Failed to update account")
        })
      },
      {
        pending: state => {
          // do nothing
        },
        fulfilled: (state, action) => {
          const { user_account_id, email, username, password } = action.payload
          if (state.current && state.current.user_account_id === user_account_id) {
            // response is valid
            state.current.email = email
            state.current.username = username
            state.current.password = password
          } 
          else {
            // the user closed account information view or response expired, do nothing
            console.warn(`Incoming account update, but the account view expired.`)
            console.log("Response is ignored.")
          }
        },
        rejected: state => {
          console.error("Failed to update account")
        },
      },
    ),

    // Define async thunk for deleting account
    deleteAccount: create.asyncThunk(
      async (): 
      Promise<any> => {
        fetch(`${server_base_url}/delete_account`, {
          method: "DELETE",
          credentials: "same-origin", // to enable cookies so that user account id can get through
        }).then(response => {
          if (!response.ok) {
            console.error("Failed to delete account")
          }
        })
      },
      {
        pending: state => {
          // do nothing
        },
        fulfilled: (state, action) => {
          if (action.payload === null) {
            state.current = null
          }
          else {
            // the user closed account creation view or response expired, do nothing
            console.warn(`Incoming account deletion, but the session expired.`)
            console.log("Response is ignored.")
          }
        },
        rejected: state => {
          console.error("Failed to delete account")
        },
      },
    ),
  }),
})

export const {createAccount, updateAccount, deleteAccount, fetchAccountInfo} = accountSlice.actions