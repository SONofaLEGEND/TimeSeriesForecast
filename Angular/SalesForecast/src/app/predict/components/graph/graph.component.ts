import { Component, OnInit } from '@angular/core';
import { FileService } from '../../services/file.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit{
  private file: File | null = null;

  constructor(private fileService: FileService, private http:HttpClient) {}

  ngOnInit() {
    this.fileService.file$.subscribe(file => {
      if (file) {
        console.log('Processing file:', file.name);
        const formData = new FormData();
        formData.append('file', file);
      
        this.http.post('http://localhost:5000/predict', formData).subscribe(
          (response) => {console.log(response);
                        },
          (error) => console.log(error)
        );
          } else {
            console.error('No file selected');
          }
        });
  }
}
