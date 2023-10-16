import { authApi, noAuthApi, countriesApi } from "./api";
import { endPoints } from "./resources";

/**
 * AuthService is responsible for authenticating a user.
 */

export class AuthService {
  /** getCountries function fetches a list of countries
   *
   * @returns call codes and flags
   */
  static async getCountries() {
    try {
      const data = await countriesApi.get();
      console.log(data, "data");
      return data;
    } catch (error) {
      console.log(error, "caught error");
    }
  }

  /** createNewUser function creates a new user account
   *
   * @returns access token and refresh token
   */
  static async createNewUser(formData) {
    try {
      console.log(formData, "from the service");
      const data = await noAuthApi.post(endPoints.signUp, formData);
      console.log(data, "data");
      return data;
    } catch (error) {
      console.log(error, "datadbklbdb");
    }
  }
}
