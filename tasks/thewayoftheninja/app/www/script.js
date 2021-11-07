var imgstr = ['1.png','2.png','3.png','4.png','5.png'];
var imgx = [800,100,12,100,5];
var imgy = [600,71,39,35,5];
var imgs = [];
var youx = 100, youy = 400;
var youstepx=4,youstepy=3;
var youmovex=0,youmovey=0;
var buls = [];
var ebuls = [];
var enemies = [];
var score = 0, endgame = 0, tcount=0;

function cls_ene_bul(i,j)
{
	var x1 = enemies[i].x, y1 = enemies[i].y;
	var x2 = buls[j].x, y2 = buls[j].y;
	
	if ( (x2+imgx[2]>x1)&&(x1+imgx[3]>x2)&&(y2+imgy[2]>y1)&&(y1+imgy[3]>y2) )
	{
		enemies.splice(i,1);
		buls.splice(j,1);
		score+=10;
		return 1;
	}
	return 0;
}

function cls_you_ebul(j)
{
	var x1 = youx, y1 = youy;
	var x2 = ebuls[j].x, y2 = ebuls[j].y;
	
	if ( (x2+imgx[4]>x1)&&(x1+imgx[1]>x2)&&(y2+imgy[4]>y1)&&(y1+imgy[1]>y2) )
	{
		endgame = 1;
		alert('Вы набрали '+score+' очков. Обновите страницу чтобы начать новую игру.');
		return 1;
	}
	return 0;
}

function new_bullet()
{
	var tmp = {};
	tmp.x=youx+33;
	tmp.y=youy-20;
	
	buls.push(tmp);

}

function new_ebullet(i)
{
	var tmp = {};
	tmp.x=enemies[i].x+Math.floor(imgx[3]/2);
	tmp.y=enemies[i].y+imgy[3]+2;
	
	ebuls.push(tmp);

}

function new_enemies()
{
	if (enemies.length>0) return;
	
	for (var i=0;i<5;i++)
	{
		var tmp = {};
		tmp.x=i*160+20;
		tmp.y=100;
		enemies.push(tmp);
	}
}

function move_bullets()
{
	var bul_del = 0;
	for (var i=buls.length-1;i>=0;i--)
	{
		bul_del = 0;
		buls[i].y-=7;
		for (var j=enemies.length-1;j>=0;j--)
		{
			if (bul_del==0)
				if (cls_ene_bul(j,i) == 1) 
					bul_del = 1;
		}		
		
		if (bul_del==0)
			if (buls[i].y<-40)
				buls.splice(i,1);
	}
}

function move_ebullets()
{

	for (var i=ebuls.length-1;i>=0;i--)
	{
		ebuls[i].y+=7;
		if (cls_you_ebul(i) == 1) 
			return 1;	
		

		if (ebuls[i].y>550)
			ebuls.splice(i,1);
	}
}

function move_you(e)
{
	if (endgame == 1) return;
	if (e.keyCode==37)
		{youmovex = -1; youmovey = 0;}
	if (e.keyCode==39)
		{youmovex = 1; youmovey = 0;}
		
	if (e.keyCode==38)
		{youmovex = 0; youmovey = -1;}
	if (e.keyCode==40)
		{youmovex = 0; youmovey = 1;}
	if (e.keyCode==32)
		new_bullet();
		
	
}

function timer()
{
if (endgame == 1) return;
tcount++;

if (youx >= 800-5-imgx[1])
	{ youmovex = -1; youmovey = 0; }
if (youx <= 0+5)
	{ youmovex = 1; youmovey = 0; }
if (youy >= 600-5-imgy[1])
	{ youmovey = -1; youmovex = 0; }
if (youy <= 200+5)
	{ youmovey = 1; youmovex = 0; }

youx += youmovex*youstepx;
youy += youmovey*youstepy;

if (tcount % 50 == 0)
{
	for (var i=0;i<enemies.length;i++)
	{
		if (Math.random()<0.2+Math.min(0.1,0.001*(tcount % 100) ) )
			new_ebullet(i);
	}
}

move_bullets();
if (move_ebullets() == 1) return;
new_enemies();
document.onkeydown = move_you;
draw();
window.setTimeout("timer();", 20);
}

function ImagesInit()
{
  for (var i=0;i<=4;i++)
  {
    var tmp = new Image();
    tmp.src = imgstr[i];
    imgs.push(tmp);
  }
  
}

function draw()
{
	ImagesInit();
	var cnv = document.getElementById("canvas");
	var ctx = cnv.getContext("2d");
	
	ctx.drawImage(imgs[0],0,0);
	ctx.drawImage(imgs[1],youx,youy);
	
	for (var i=0;i<buls.length;i++)
	{
		ctx.drawImage(imgs[2],buls[i].x,buls[i].y);
	}
	
	for (var i=0;i<enemies.length;i++)
	{
		ctx.drawImage(imgs[3],enemies[i].x,enemies[i].y);
	}
	
	for (var i=0;i<ebuls.length;i++)
	{
		ctx.drawImage(imgs[4],ebuls[i].x,ebuls[i].y);
	}	
	ctx.fillStyle = "#FFFF00";
	ctx.font = "bold 30pt Arial";
	ctx.fillText(score+'',50,50);
	ctx.fillText(youx+' '+youy,550,50);
}
document.getelemtByID.innerHtml = "https://media.vanityfair.com/photos/55d4ee7f169027501c6fa604/master/w_2560%2Cc_limit/vin-diesel-royal-doppleganger.jpg"
window.addEventListener("load",draw,true);