import { Component, OnInit } from '@angular/core';
import { MatDatepickerInputEvent } from '@angular/material';
import { EventService } from '../event.service';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-date-picker',
  templateUrl: './date-picker.component.html',
  styleUrls: ['./date-picker.component.scss']
})
export class DatePickerComponent implements OnInit {
  date = new FormControl(new Date());
  constructor(private eventService: EventService) { }

  ngOnInit() {
    this.eventService.dateChange(new Date());
  }

  dateChanged(event: MatDatepickerInputEvent<Date>) {
    this.eventService.dateChange(event.value);
  }
}
