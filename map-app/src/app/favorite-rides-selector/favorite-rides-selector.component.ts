import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { ServerApiService } from '../server-api.service';

interface FavoriteRide {
  rideName: string;
  isFavoriteRide: boolean;
}

@Component({
  selector: 'app-favorite-rides-selector',
  templateUrl: './favorite-rides-selector.component.html',
  styleUrls: ['./favorite-rides-selector.component.scss']
})
export class FavoriteRidesSelectorComponent implements OnInit {
  userName: string;
  password: string;
  isDisabled = true;

  constructor(public dialogRef: MatDialogRef<FavoriteRidesSelectorComponent>, private serverApiService: ServerApiService,
              @Inject(MAT_DIALOG_DATA) public rides: FavoriteRide[]) { }

  ngOnInit() {
  }

  onSetRidesClick(): void {
    const favoriteRides = []
    for (const ride of this.rides) {
      if (ride.isFavoriteRide) {
        favoriteRides.push(ride.rideName);
      }
    }
    this.serverApiService.setFavoriteRides({favorite_rides: favoriteRides}).subscribe(res => {
      this.dialogRef.close();
    }, err => {
      console.log(err);
    });
  }

  onCancelClick(): void {
    this.dialogRef.close();
  }
}
