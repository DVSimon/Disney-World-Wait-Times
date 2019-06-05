import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AgmCoreModule, GoogleMapsAPIWrapper } from '@agm/core';
import { MapComponent } from './map/map.component';
import { HttpClientModule } from '@angular/common/http';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule, MatFormFieldModule, MatTableModule, MatInputModule, MatSelectModule,
  MatDatepickerModule, MatNativeDateModule, MatDialogModule, MatButtonModule, MatSnackBarModule,
  MatCheckboxModule } from '@angular/material';
import { TableComponent } from './table/table.component';
import { ChartComponent } from './chart/chart.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { FlexLayoutModule } from '@angular/flex-layout';
import { RideFilterComponent } from './ride-filter/ride-filter.component';
import { FormsModule } from '@angular/forms';
import { DatePickerComponent } from './date-picker/date-picker.component';
import { LoginComponent } from './login/login.component';
import { CreateUserComponent } from './create-user/create-user.component';
import { FavoriteRidesComponent } from './favorite-rides/favorite-rides.component';
import { FavoriteRidesSelectorComponent } from './favorite-rides-selector/favorite-rides-selector.component';
import { UserProfileComponent } from './user-profile/user-profile.component';

@NgModule({
  imports: [
    BrowserModule,
    AppRoutingModule,
    AgmCoreModule.forRoot({
      apiKey: ''
    }),
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatTableModule,
    MatInputModule,
    NgxChartsModule,
    FlexLayoutModule,
    MatSelectModule,
    FormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,
    MatDialogModule,
    MatSnackBarModule,
    MatCheckboxModule
  ],
  declarations: [
    AppComponent,
    MapComponent,
    ToolbarComponent,
    TableComponent,
    ChartComponent,
    RideFilterComponent,
    DatePickerComponent,
    LoginComponent,
    CreateUserComponent,
    FavoriteRidesComponent,
    FavoriteRidesSelectorComponent,
    UserProfileComponent
  ],
  entryComponents: [
    LoginComponent,
    CreateUserComponent,
    FavoriteRidesSelectorComponent
  ],
  providers: [
    GoogleMapsAPIWrapper
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
