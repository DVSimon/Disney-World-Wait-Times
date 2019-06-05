import { Component, OnInit } from '@angular/core';
import { MatDialogRef, MatSnackBar, MatSnackBarRef, SimpleSnackBar } from '@angular/material';
import { ServerApiService } from '../server-api.service';

interface CreateUserResponse {
  status: string;
  token: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './create-user.component.html',
  styleUrls: ['./create-user.component.scss']
})
export class CreateUserComponent implements OnInit {
  userName: string;
  password: string;
  reenterPassword: string;
  isDisabled = true;
  snackBarRef: MatSnackBarRef<SimpleSnackBar>;

  constructor(public dialogRef: MatDialogRef<CreateUserComponent>, private serverApiService: ServerApiService,
              private snackBar: MatSnackBar) { }

  ngOnInit() {
  }

  onLoginClick(): void {
    if (this.snackBarRef) {
      this.snackBarRef.dismiss();
    }
    if (this.password !== this.reenterPassword) {
      this.snackBarRef = this.snackBar.open('Passwords don\'t match', null, {
          duration: 9000
      });
      return;
    }
    this.serverApiService.createUser({
      user_name: this.userName,
      password: this.password
    }).subscribe( (res: CreateUserResponse) => {
      localStorage.setItem('rides_app_token', res.token);
      location.reload();
    }, error => {
      console.log(error);
      this.snackBarRef = this.snackBar.open('User name already exists', null, {
        duration: 9000
      });
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }

  updateLoginButton(): void {
    this.isDisabled = !this.userName || !this.password || !this.reenterPassword ||
        this.userName.length === 0 || this.password.length === 0 || this.reenterPassword.length === 0;
  }
}
