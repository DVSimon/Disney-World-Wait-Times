import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { EventService } from '../event.service';
import { ServerApiService } from '../server-api.service';
@Component({
  selector: 'app-chart',
  template: '<h3 class="chart-title" >{{chartTitle}}</h3>\n' +
      '<ngx-charts-line-chart\n' +
      '        [view]="view"\n' +
      '        [scheme]="colorScheme"\n' +
      '        [results]="multi"\n' +
      '        [gradient]="gradient"\n' +
      '        [xAxis]="showXAxis"\n' +
      '        [yAxis]="showYAxis"\n' +
      '        [legend]="showLegend"\n' +
      '        [showXAxisLabel]="showXAxisLabel"\n' +
      '        [showYAxisLabel]="showYAxisLabel"\n' +
      '        [xAxisLabel]="xAxisLabel"\n' +
      '        [yAxisLabel]="yAxisLabel"\n' +
      '        [autoScale]="autoScale"></ngx-charts-line-chart>',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit {
  eventDateChangeSubscription: Subscription;
  eventRideChangeSubscription: Subscription;
  month: number;
  day: number;
  year: number;
  dayOfWeek: number;
  selectedRide: string;
  chartTitle = '';
  multi: any[] = [{
    name: 'Estimated Wait Time',
    series: [
      {
        name: '8am',
        value: 0
      },
      {
        name: '9am',
        value: 0
      },
      {
        name: '10am',
        value: 0
      },
      {
        name: '11am',
        value: 0
      },
      {
        name: '12pm',
        value: 0
      },
      {
        name: '1pm',
        value: 0
      },
      {
        name: '2pm',
        value: 0
      },
      {
        name: '3pm',
        value: 0
      },
      {
        name: '4pm',
        value: 0
      },
      {
        name: '5pm',
        value: 0
      },
      {
        name: '6pm',
        value: 0
      },
      {
        name: '7pm',
        value: 0
      },
      {
        name: '8pm',
        value: 0
      },
      {
        name: '9pm',
        value: 0
      },
      {
        name: '10pm',
        value: 0
      },
      {
        name: '11pm',
        value: 0
      },
      {
        name: '12am',
        value: 0
      }
    ]
  }];
  chartHeight = 700;
  view: any[] = (typeof window.orientation !== 'undefined') ? [400, 400] : [700, 400];
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Time';
  showYAxisLabel = true;
  yAxisLabel = 'Wait Time';
  autoScale = true;
  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };
  isLoggedIn = false;

  constructor(private eventService: EventService, private serverApiService: ServerApiService) {
    this.eventService.userChange$.subscribe(user => {
      this.isLoggedIn = true;
    });

    const date = new Date();
    this.month = date.getMonth() + 1;
    this.day = date.getDate();
    this.dayOfWeek = this.mapDayOfWeek(date.getDay());
    this.year = date.getFullYear();
    this.selectedRide = 'Alien Swirling Saucers';
    this.sendPredictRequest();
  }

  ngOnInit() {
    this.eventDateChangeSubscription = this.eventService.dateChange$.subscribe( dateChange => {
      if (dateChange) {
        this.month = dateChange.getMonth() + 1;
        this.day = dateChange.getDate();
        this.dayOfWeek = this.mapDayOfWeek(dateChange.getDay());
        this.year = dateChange.getFullYear();
        this.chartTitle = `${this.selectedRide}  ${this.month}/${this.day}/${this.year}`;
        this.sendPredictRequest();
      }
    });

    this.eventRideChangeSubscription = this.eventService.rideChange$.subscribe( rideChange => {
      if (rideChange) {
        this.selectedRide = rideChange.ride;
        this.chartTitle = `${this.selectedRide}  ${this.month}/${this.day}/${this.year}`;
        this.sendPredictRequest();
      }
    });
  }

  sendPredictRequest() {
    this.serverApiService.getPrediction({
      ride: `${this.selectedRide}`,
      month: `${this.month}`,
      day: `${this.day}`,
      year: `${this.year}`,
      dayofweek: `${this.dayOfWeek}`
    }).subscribe(metrics => {
      this.multi[0].series = metrics;
      this.multi = [...this.multi];

      if (this.isLoggedIn) {
        this.serverApiService.addRecentRide({ recent_ride: this.selectedRide }).subscribe( (res: any) => {
          this.serverApiService.getUserInfo().subscribe( userRes => {
            this.eventService.userChange(userRes);
          });
        });
      }
    });
  }

  mapDayOfWeek(originalDay: number) {
    if (originalDay === 0) {
      return 3;
    } else if (originalDay === 1) {
      return 1;
    } else if (originalDay === 2) {
      return 5;
    } else if (originalDay === 3) {
      return 6;
    } else if (originalDay === 4) {
      return 4;
    } else if (originalDay === 5) {
      return 0;
    } else if (originalDay === 6) {
      return 2;
    }
  }
}
