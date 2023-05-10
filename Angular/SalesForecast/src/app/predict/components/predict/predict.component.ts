import { Component } from '@angular/core';
import { FileService } from '../../services/file.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css']
})
export class PredictComponent {
  correctFile: boolean = false;
  errorMessage:String;
  constructor(private fileService: FileService, private router:Router) {}

  
  onFileSelected(event: any) {

    const file: File = event.target.files[0];
    if (file.type !== 'text/csv') {
      this.errorMessage = 'Invalid file format. Please upload a CSV file.';
      this.correctFile = false;

      return;
    }
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
      const csvData: string = reader.result.toString();
      const rows = csvData.split('\n');
      const headers = rows[0].toLowerCase().split(',');
      const requiredFields = ['order date', 'sales'].map(field => field.toLowerCase());
      if (!requiredFields.every(field => headers.includes(field))) {
        this.errorMessage = 'CSV file is missing required fields.';
        this.correctFile = false;
        return;
      }
      
    };
    this.fileService.setFile(file);
    this.correctFile = true;
  }
  navPredict(){
    this.router.navigate(['/graph'])
  }
  
}
