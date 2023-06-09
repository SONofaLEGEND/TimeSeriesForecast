import { Injectable } from "@angular/core";
import { CanActivate } from "@angular/router";
import { Router } from "@angular/router";
import { CookieService } from "ngx-cookie-service";

@Injectable({
    providedIn: 'root'
  })
  export class AuthGuard implements CanActivate {
    constructor(private router: Router, private cookieService:CookieService) {}
  
    canActivate(): boolean {
      if (this.cookieService.get('token')) {
        return true;
      }
      this.router.navigate(['\login']);
      return false;
    }
    
  }