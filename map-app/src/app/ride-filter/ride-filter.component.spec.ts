import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RideFilterComponent } from './ride-filter.component';

describe('RideFilterComponent', () => {
  let component: RideFilterComponent;
  let fixture: ComponentFixture<RideFilterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RideFilterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RideFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
