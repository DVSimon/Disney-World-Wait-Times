import { Component, OnInit } from '@angular/core';
import { Ride } from '../ride';
import { EventService } from '../event.service';
import { ServerApiService } from '../server-api.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent implements OnInit {
  imageUrl: string;
  userName: string;
  favoriteRides: string[];
  recentRides: string[];
  constructor(private eventService: EventService, private serverAPIService: ServerApiService) {
    this.eventService.userChange$.subscribe(user => {
      this.userName = user.userName;
      this.imageUrl = user.image;
      this.favoriteRides = user.favorite_rides;
      this.recentRides = user.recent_rides;
    });
  }

  ngOnInit() {
  }

  onImageChange(event) {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]); // read file as data url
      reader.onload = (eventRead: any) => { // called once readAsDataURL is completed
        this.imageUrl = eventRead.target.result;
        this.serverAPIService.setUserImage({image: this.imageUrl}).subscribe(res => {
        });
      };
    }
  }

  deleteUser() {
    this.serverAPIService.deleteUser().subscribe(res => {
      localStorage.removeItem('rides_app_token');
      location.reload();
    });
  }
}
