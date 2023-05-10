import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor() { }
  private fileSubject = new BehaviorSubject<File | null>(null);
  public file$ = this.fileSubject.asObservable();

  public setFile(file: File) {
    this.fileSubject.next(file);
  }
}
