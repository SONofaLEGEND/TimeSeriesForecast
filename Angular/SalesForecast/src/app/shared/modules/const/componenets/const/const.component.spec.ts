import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConstComponent } from './const.component';

describe('ConstComponent', () => {
  let component: ConstComponent;
  let fixture: ComponentFixture<ConstComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ConstComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConstComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
