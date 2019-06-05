import { Component } from '@angular/core';
import {EventService} from './event.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'map-app';
  showApp = true;
  isMobile = false;

  constructor(private eventService: EventService) {
    if (typeof window.orientation !== 'undefined') {
      this.isMobile = true;
    }
    this.eventService.mapAppChangeSource$.subscribe( isMapAppClicked => {
      this.showApp = isMapAppClicked;
    });
  }
}
