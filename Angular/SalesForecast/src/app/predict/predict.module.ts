import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictComponent } from './components/predict/predict.component';
import { RouterModule } from '@angular/router';
import { BackendErrorMessagesModule } from '../auth/types/modules/backendErrorMessages/backendErrorMessages.module';
import { GraphComponent } from './components/graph/graph.component';
import { AuthGuard } from '../shared/services/auth.guard';

const routes = [
{
  path: 'predict',
  component: PredictComponent,
  canActivate: [AuthGuard]
},
{
  path: 'graph',
  component: GraphComponent
}
]

@NgModule({
  declarations: [
    PredictComponent,
    GraphComponent
  ],
  imports: [
    CommonModule,
    BackendErrorMessagesModule,

    RouterModule.forChild(routes),
  ]
})
export class PredictModule { }
