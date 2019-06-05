import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Ride } from './ride';

interface RideChange {
  ride: string;
  adjust: boolean;
}

interface User {
  userName: string;
  image: string;
  favorite_rides: string[];
  recent_rides: string[];
}

@Injectable({
  providedIn: 'root'
})
export class EventService {

  constructor() { }

  private parkFilterSource = new Subject<string>();
  private dateChangeSource = new Subject<Date>();
  private rideChangeSource = new Subject<RideChange>();
  private userChangeSource = new Subject<User>();
  private mapAppChangeSource = new Subject<boolean>();

  parkFilter$ = this.parkFilterSource.asObservable();
  dateChange$ = this.dateChangeSource.asObservable();
  rideChange$ = this.rideChangeSource.asObservable();
  userChange$ = this.userChangeSource.asObservable();
  mapAppChangeSource$ = this.mapAppChangeSource.asObservable();

  parkFilter(mission: string) {
    this.parkFilterSource.next(mission);
  }

  dateChange(date: Date) {
    this.dateChangeSource.next(date);
  }

  rideChange(rideName: string, readjustMap: boolean) {
    this.rideChangeSource.next({ride: rideName, adjust: readjustMap});
  }

  userChange(user: User) {
    this.userChangeSource.next(user);
  }

  mapAppChange(mapAppSelected: boolean) {
    this.mapAppChangeSource.next(mapAppSelected);
  }
}
