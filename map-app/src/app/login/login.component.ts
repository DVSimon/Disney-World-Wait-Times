import { Component, OnInit } from '@angular/core';
import { MatDialogRef, MatSnackBar, MatSnackBarRef, SimpleSnackBar } from '@angular/material';
import { ServerApiService } from '../server-api.service';

interface LoginResponse {
  status: string;
  token: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  userName: string;
  password: string;
  isDisabled = true;
  snackBarRef: MatSnackBarRef<SimpleSnackBar>;

  constructor(public dialogRef: MatDialogRef<LoginComponent>, private serverApiService: ServerApiService,
              private snackBar: MatSnackBar) { }

  ngOnInit() {
  }

  onLoginClick(): void {

    this.serverApiService.login({
      user_name: this.userName,
      password: this.password
    }).subscribe( (res: LoginResponse) => {
      if (this.snackBarRef) {
        this.snackBarRef.dismiss();
      }
      localStorage.setItem('rides_app_token', res.token);
      location.reload();
    }, error => {
      this.snackBarRef = this.snackBar.open('Login Failed', null, {
        duration: 9000,
      });
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  updateLoginButton(): void {
    this.isDisabled = !this.userName || !this.password ||   this.userName.length === 0 || this.password.length === 0;
  }
}
