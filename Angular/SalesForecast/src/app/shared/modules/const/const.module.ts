import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConstComponent } from './componenets/const/const.component';
import { Router, RouterModule } from '@angular/router';

const routes = [
  {
    path: 'const',
    component: ConstComponent
  }
]

@NgModule({
  declarations: [
    ConstComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    
  ]
})
export class ConstModule { }
