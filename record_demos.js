const { chromium } = require('playwright');
const path = require('path');

const roles = [
  { username: 'admin', password: 'admin123', pages: ['Tableau de Bord', 'Personnel', 'Paie & Frais', 'Congés', 'Objectifs', 'Pointage', 'Recrutement'] },
  { username: 'rh', password: 'rh123', pages: ['Tableau de Bord', 'Personnel', 'Paie & Frais', 'Congés', 'Objectifs', 'Pointage', 'Recrutement'] },
  { username: 'manager', password: 'manager123', pages: ['Tableau de Bord', 'Paie & Frais', 'Congés', 'Objectifs'] },
  { username: 'employe', password: 'employe123', pages: ['Paie & Frais', 'Congés', 'Objectifs', 'Pointage'] },
  { username: 'auditeur', password: 'auditeur123', pages: ['Tableau de Bord', 'Personnel', 'Paie & Frais'] },
  { username: 'candidat', password: 'candidat123', pages: ['Recrutement'] }
];

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function run() {
  for (const role of roles) {
    console.log(`Recording test for role: ${role.username}...`);
    const browser = await chromium.launch({ headless: true });
    
    // Create a new context with video recording enabled
    const context = await browser.newContext({
      recordVideo: {
        dir: path.join(__dirname, 'demo_videos'),
        size: { width: 1280, height: 720 }
      },
      viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    try {
      await page.goto('http://localhost:5173/');
      await sleep(1000);
      
      // Login
      await page.fill('#login_username', role.username);
      await page.fill('#login_password', role.password);
      await page.click('button[type="submit"]');
      await sleep(2000); // Wait for login and redirect
      
      // Navigate pages
      for (const menuItem of role.pages) {
        console.log(`  Navigating to ${menuItem}`);
        // Click on the menu item by text
        await page.click(`text=${menuItem}`);
        await sleep(2000); // Wait for page to render and let it be recorded
      }
      
      // Logout
      await page.click('text=Déconnexion');
      await sleep(1000);
      
    } catch (e) {
      console.error(`Error during recording for ${role.username}:`, e);
    } finally {
      // Close page and context to save the video
      await page.close();
      await context.close();
      
      // The video is saved with a random string, we should rename it
      const fs = require('fs');
      const files = fs.readdirSync(path.join(__dirname, 'demo_videos'));
      const videoFile = files.find(f => f.endsWith('.webm') && !f.startsWith('demo_'));
      if (videoFile) {
        fs.renameSync(
          path.join(__dirname, 'demo_videos', videoFile),
          path.join(__dirname, 'demo_videos', `demo_role_${role.username}.webm`)
        );
      }
      
      await browser.close();
      console.log(`Finished recording for ${role.username}.`);
    }
  }
}

run().catch(console.error);
