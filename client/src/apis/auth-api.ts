export class AuthApi {
  async login(email: string, password: string) {
    console.log(email, password);
  }

  async signUp(data: any) {
    console.log(data);
  }
}
