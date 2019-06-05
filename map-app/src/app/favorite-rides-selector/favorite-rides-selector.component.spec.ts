import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteRidesSelectorComponent } from './favorite-rides-selector.component';

describe('FavoriteRidesSelectorComponent', () => {
  let component: FavoriteRidesSelectorComponent;
  let fixture: ComponentFixture<FavoriteRidesSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteRidesSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteRidesSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
