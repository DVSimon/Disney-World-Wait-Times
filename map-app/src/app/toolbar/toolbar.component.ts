import { Component, OnInit } from '@angular/core';
import { LoginComponent } from '../login/login.component';
import { MatDialog } from '@angular/material';
import { EventService } from '../event.service';
import { CreateUserComponent } from '../create-user/create-user.component';
import { ServerApiService } from '../server-api.service';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {
  userName = '';
  isLoggedIn = false;
  constructor(public dialog: MatDialog, private eventService: EventService, private serverAPIService: ServerApiService) {
    this.eventService.userChange$.subscribe(user => {
      this.userName = user.userName;
      this.isLoggedIn = true;
    });
  }

  ngOnInit() {
  }

  login() {
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '250px'
    });

    dialogRef.afterClosed().subscribe(result => {
    });
  }

  createUser() {
    const dialogRef = this.dialog.open(CreateUserComponent, {
      width: '350px'
    });

    dialogRef.afterClosed().subscribe(result => {
    });
  }

  logout() {
    this.serverAPIService.logout().subscribe(res => {
      localStorage.removeItem('rides_app_token');
      location.reload();
    }, err => {
      localStorage.removeItem('rides_app_token');
      location.reload();
    });
  }

  triggerUserClickEvent(isMapAppClicked: boolean) {
    this.eventService.mapAppChange(isMapAppClicked);
    this.serverAPIService.getUserInfo().subscribe(user => {
      this.eventService.userChange(user);
    });
  }
}
