import { Component, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { MapsAPILoader, AgmMap } from '@agm/core';
import { ServerApiService } from '../server-api.service';
import { Subscription } from 'rxjs';
import { EventService } from '../event.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, OnDestroy {

  @ViewChild(AgmMap) map: AgmMap;
  lat: number;
  lng: number;
  zoom: number;
  public mapStyles = [
    {
      featureType: 'poi',
      elementType: 'labels',
      stylers: [
        {
          visibility: 'off'
        }
      ]
    }
  ];
  visibleRides = [];
  totalRides = [];
  parksSubscription: Subscription;
  eventServiceSubscription: Subscription;
  favoriteRides: string[];
  recentRides: string[];
  parkFilter = 'All Parks';

  constructor(public mapsApiLoader: MapsAPILoader, private serverApiService: ServerApiService, private eventService: EventService) {
    eventService.userChange$.subscribe(res => {
      this.favoriteRides = res.favorite_rides;
      this.recentRides = res.recent_rides;
      if (this.parkFilter === 'Favorite Rides' || this.parkFilter === 'Recent Rides') {
        this.updateMarkers();
      }
    });
  }

  ngOnInit() {
    // Load map and center it on theme park
    this.mapsApiLoader.load().then(() => {
      this.lat = 28.355811;
      this.lng = -81.5637406;
      this.zoom = 18;
    });

    // Get list of rides from server
    this.parksSubscription = this.serverApiService.getParks().subscribe(res => {
      const keys = Object.keys(res.body);
      for (const key of keys) {
        const parkRides = res.body[key].rides;
        const rideParkName = res.body[key].parkName;
        for (const ride of parkRides) {
          this.totalRides.push({
            rideName: ride.rideName,
            lat: ride.lat,
            lng: ride.lng,
            parkName: rideParkName
          });
          this.visibleRides.push(ride);
        }
      }
    });

    this.eventServiceSubscription = this.eventService.parkFilter$.subscribe(parkFilter => {
      this.parkFilter = parkFilter;
      this.updateMarkers();
    });

    this.eventServiceSubscription = this.eventService.rideChange$.subscribe(rideChange => {
      if (rideChange.adjust) {
        for (const ride of this.visibleRides) {
          if (ride.rideName === rideChange.ride) {
            this.lat = ride.lat;
            this.lng = ride.lng;
          }
        }
      }
    });
  }

  handleRideClick(ride) {
    this.eventService.rideChange(ride.rideName, false);
  }

  ngOnDestroy() {
    if (this.parksSubscription) {
      this.parksSubscription.unsubscribe();
    }
  }

  updateMarkers() {
    this.visibleRides = [];
    for (const ride of this.totalRides) {
      if (ride.parkName === this.parkFilter || this.parkFilter === 'All Parks' ||
          (this.parkFilter === 'Favorite Rides' && this.favoriteRides.indexOf(ride.rideName) > -1) ||
          (this.parkFilter === 'Recent Rides' && this.recentRides.indexOf(ride.rideName) > -1)) {
        this.visibleRides.push(ride);
      }
    }
  }
}
