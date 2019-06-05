import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FavoriteRidesComponent } from './favorite-rides.component';

describe('FavoriteRidesComponent', () => {
  let component: FavoriteRidesComponent;
  let fixture: ComponentFixture<FavoriteRidesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FavoriteRidesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FavoriteRidesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
