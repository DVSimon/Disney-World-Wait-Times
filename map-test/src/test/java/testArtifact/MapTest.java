package testArtifact;

import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class MapTest {
	public static WebDriver driver;

	@Test
	public void createUser() throws InterruptedException {
		WebElement loginButton = driver.findElement(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/button[2]"));
		loginButton.click();
		driver.findElement(By.xpath("//*[@id=\"mat-input-2\"]")).sendKeys("TestUser");;
		driver.findElement(By.xpath("//*[@id=\"mat-input-3\"]")).sendKeys("pass");
		driver.findElement(By.xpath("//*[@id=\"mat-input-4\"]")).sendKeys("pass");
		driver.findElement(By.xpath("//*[@id=\"mat-dialog-0\"]/app-login/div[2]/button[1]")).click();
		WebDriverWait wait = new WebDriverWait(driver, 10);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/span[3]")));
		WebElement userSpan = driver.findElement(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/span[3]"));
	    Assert.assertEquals(userSpan.getText(), "TestUser");
	}
	
	
	@Test
	public void clickRides() throws InterruptedException {
		WebDriverWait wait = new WebDriverWait(driver, 10);
		for (int i = 0; i < 14; i++) {
			driver.findElement(By.xpath("//*[@id=\"mat-input-0\"]")).sendKeys(Keys.BACK_SPACE);
		}
		driver.findElement(By.xpath("//*[@id=\"mat-input-0\"]")).clear();
		driver.findElement(By.xpath("//*[@id=\"mat-input-0\"]")).sendKeys("5/1/2019");
		driver.findElement(By.xpath("//*[@id=\"mat-input-0\"]")).sendKeys(Keys.TAB);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("/html/body/app-root/div/div/div[1]/app-chart/h3")));
		WebElement chartTitle = driver.findElement(By.xpath("/html/body/app-root/div/div/div[1]/app-chart/h3"));
		Thread.sleep(2000);
		driver.findElement(By.xpath("/html/body/app-root/div/div/app-table/div/table/tbody/tr[2]")).click();
		Assert.assertEquals(chartTitle.getText(), "Rock 'n' Roller Coaster 5/1/2019");
		Thread.sleep(2000);
		driver.findElement(By.xpath("/html/body/app-root/div/div/app-table/div/table/tbody/tr[3]")).click();
		Assert.assertEquals(chartTitle.getText(), "Slinky Dog Dash 5/1/2019");
		Thread.sleep(2000);
		driver.findElement(By.xpath("/html/body/app-root/div/div/app-table/div/table/tbody/tr[4]")).click();
		Assert.assertEquals(chartTitle.getText(), "Toy Story Mania! 5/1/2019");
		Thread.sleep(2000);
		driver.findElement(By.xpath("/html/body/app-root/div/div/app-table/div/table/tbody/tr[5]")).click();
		Assert.assertEquals(chartTitle.getText(), "Avatar Flight of Passage 5/1/2019");
	}

	@Test
	public void selectFavoriteRides() throws InterruptedException {
		WebDriverWait wait = new WebDriverWait(driver, 10);
		driver.findElement(By.xpath("/html/body/app-root/div/div/div[2]/app-favorite-rides/button")).click();
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//*[@id=\"mat-checkbox-7\"]/label/div")));
		driver.findElement(By.xpath("//*[@id=\"mat-checkbox-7\"]/label/div")).click();
		driver.findElement(By.xpath("//*[@id=\"mat-checkbox-8\"]/label/div")).click();
		driver.findElement(By.xpath("//*[@id=\"mat-dialog-0\"]/app-favorite-rides-selector/div[2]/button[1]")).click();
		Thread.sleep(2000);
	}
	
	@Test
	public void checkProfilePage() throws InterruptedException {
		driver.findElement(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/span[3]")).click();
		WebDriverWait wait = new WebDriverWait(driver, 10);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("/html/body/app-root/div/div/app-user-profile/div/button")));
		Thread.sleep(2000);
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[2]/li[1]")).getText(), "Alien Swirling Saucers");
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[2]/li[2]")).getText(), "Rock 'n' Roller Coaster");
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[2]/li[3]")).getText(), "Slinky Dog Dash");
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[2]/li[4]")).getText(), "Toy Story Mania!");
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[2]/li[5]")).getText(), "Avatar Flight of Passage");
		

		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[1]/li[1]")).getText(), "Expedition Everest");
		Assert.assertEquals(driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/ul[1]/li[2]")).getText(), "Kilimanjaro Safaris");
	}
	
	@BeforeClass
	public static void beforeClass() {
		driver = new ChromeDriver();
		driver.get("http://54.201.84.148/");
	}

	@AfterClass
	public static void afterClass() {
		driver.findElement(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/span[3]")).click();
		WebDriverWait wait = new WebDriverWait(driver, 10);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("/html/body/app-root/div/div/app-user-profile/div/button")));
		driver.findElement(By.xpath("/html/body/app-root/div/div/app-user-profile/div/button")).click();
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("/html/body/app-root/div/app-toolbar/mat-toolbar/mat-toolbar-row/button[1]/span[text()=\"Login\"]")));

		driver.close();
	}

}