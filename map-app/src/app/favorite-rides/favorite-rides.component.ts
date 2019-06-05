import { Component, OnInit } from '@angular/core';
import { FavoriteRidesSelectorComponent } from '../favorite-rides-selector/favorite-rides-selector.component';
import { MatDialog } from '@angular/material';
import { EventService } from '../event.service';
import { ServerApiService } from '../server-api.service';

interface FavoriteRidesResponse {
  favoriteRides: [];
}

@Component({
  selector: 'app-favorite-rides',
  templateUrl: './favorite-rides.component.html',
  styleUrls: ['./favorite-rides.component.scss']
})
export class FavoriteRidesComponent implements OnInit {
  isLoggedIn = false;
  totalRides = [];
  favoriteRides = [];
  parks = [];

  constructor(public dialog: MatDialog, private eventService: EventService, private serverAPIService: ServerApiService) {
    const getParksSub = this.serverAPIService.getParks().subscribe(parksRes => {
      this.parks = parksRes.body;
      this.updateRides();
    });
    const userChangeSub = this.eventService.userChange$.subscribe(user => {
      this.totalRides = [];
      this.isLoggedIn = true;
      this.favoriteRides = user.favorite_rides;
      this.updateRides();
    });
  }

  ngOnInit() {
  }

  selectFavoriteRides() {
    const dialogRef = this.dialog.open(FavoriteRidesSelectorComponent, {
      width: '400px',
      data: this.totalRides
    });

    dialogRef.afterClosed().subscribe(result => {
      this.totalRides = [];
      this.favoriteRides = [];
      this.serverAPIService.getUserInfo().subscribe( res => {
          this.eventService.userChange(res);
      });
    });
  }

  private updateRides() {
    const keys = Object.keys(this.parks);
    for (const key of keys) {
      const parkRides = this.parks[key].rides;
      for (const ride of parkRides) {
        let favoriteRide = false;
        if (this.favoriteRides.indexOf(ride.rideName) > -1) {
          favoriteRide = true;
        }
        this.totalRides.push({
          rideName: ride.rideName,
          isFavoriteRide: favoriteRide
        });
      }
    }
  }
}
