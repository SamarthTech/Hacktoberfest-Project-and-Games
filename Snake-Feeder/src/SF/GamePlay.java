package SF;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;

import javax.swing.ImageIcon;
import javax.swing.JPanel;
import javax.swing.Timer;

public class GamePlay extends JPanel implements KeyListener, ActionListener{
	
	private int [] snakeXlength = new int [750];
	private int [] snakeYlength = new int [750];
	
	//check the direction of snake
	private boolean left = false;
	private boolean right = false;
	private boolean up = false;
	private boolean down = false;

	//Image of Head Position of the snake
	private ImageIcon headRight;
	private ImageIcon headLeft;
	private ImageIcon headUp;
	private ImageIcon headDown;
	
	
	//Initial length of the snake
	private int lengthOfSnake = 3;
	
	private Timer timer;
	private int delay = 100;
	
	//Image of Tail of the snake
	private ImageIcon tail;
	
	private int moves=0;
	private int score=0;	//Initial score the game
	
	//Fruit Parameters
	private int [] fruitXpos = {25,50,75,100,125,150,175,200,225,250,275,300,325,250,375,400,425,450,475,500,525,550,575,600,
			625,650,675,700,725,750,775,800,825,850};
	
	private int [] fruitYpos = {75,100,125,150,175,200,225,250,275,300,325,250,375,400,425,450,475,500,525,550,575,600,
			625};
	
	private ImageIcon fruitImage;
	
	private Random random = new Random();
	private int xpos = random.nextInt(34);
	private int ypos = random.nextInt(24);
	
	private ImageIcon titleImage;
	
	public GamePlay()
	{
		addKeyListener(this);
		setFocusable(true);
		setFocusTraversalKeysEnabled(false);
		
		timer = new Timer(delay, this);
		timer.start();
	}
	
	public void paint(Graphics g)
	{
		
		if(moves == 0)
		{
			snakeXlength[0] = 100;
			snakeXlength[1] = 75;
			snakeXlength[2] = 50;
			
			snakeYlength[0] = 100;
			snakeYlength[1] = 100;
			snakeYlength[2] = 100;

		}
		
		//Display Title
//		titleImage = new ImageIcon("res/Images/title.png");
		titleImage = new ImageIcon(getClass().getClassLoader().getResource("title.png"));
		titleImage.paintIcon(this, g, 25, 5);
		
		//Display gamePlay border
		g.setColor(Color.DARK_GRAY);
		g.drawRect(24, 74, 851, 577);
		
		//Display GamePlay Background
		g.setColor(Color.black);
		g.fillRect(25, 75, 850, 575);
		
		
		//Draw Score and length
		g.setColor(Color.white);
		g.setFont(new Font("areal", Font.PLAIN, 15));
		g.drawString("Scores:" + score, 780, 30);
		
		
		g.setColor(Color.white);
		g.setFont(new Font("areal", Font.PLAIN, 14));
		g.drawString("Length:" + lengthOfSnake, 780, 50);
		
		//Initial position of the headRight image
//		headRight = new ImageIcon("res/Images/headRight.png");
		headRight = new ImageIcon(getClass().getClassLoader().getResource("headRight.png"));
		headRight.paintIcon(this, g, snakeXlength[0], snakeYlength[0]);
		
		for(int i = 0; i < lengthOfSnake; i++)
		{
			if(i == 0 && right)
			{
//				headRight = new ImageIcon("res/Images/headRight.png");
				headRight = new ImageIcon(getClass().getClassLoader().getResource("headRight.png"));
				headRight.paintIcon(this, g, snakeXlength[i], snakeYlength[i]);
			}
			
			if(i == 0 && left)
			{
//				headLeft = new ImageIcon("res/Images/headLeft.png");
				headLeft = new ImageIcon(getClass().getClassLoader().getResource("headLeft.png"));
				headLeft.paintIcon(this, g, snakeXlength[i], snakeYlength[i]);
			}
			
			if(i == 0 && up)
			{
//				headUp = new ImageIcon("res/Images/headUp.png");
				headUp = new ImageIcon(getClass().getClassLoader().getResource("headUp.png"));
				headUp.paintIcon(this, g, snakeXlength[i], snakeYlength[i]);
			}
			
			if(i == 0 && down)
			{
//				headDown = new ImageIcon("res/Images/headDown.png");
				headDown = new ImageIcon(getClass().getClassLoader().getResource("headDown.png"));
				headDown.paintIcon(this, g, snakeXlength[i], snakeYlength[i]);
			}
			
			//When we are in tail position
			if(i!=0)
			{
//				tail = new ImageIcon("res/Images/tail.png");
				tail = new ImageIcon(getClass().getClassLoader().getResource("tail.png"));
				tail.paintIcon(this, g, snakeXlength[i], snakeYlength[i]);
			}
			
			//Fruit Image
//			fruitImage = new ImageIcon("res/Images/fruit.png");
			fruitImage = new ImageIcon(getClass().getClassLoader().getResource("fruit.png"));
			
			if(fruitXpos[xpos] == snakeXlength[0] && fruitYpos[ypos] == snakeYlength[0])
			{
				score+=5;
				lengthOfSnake++;
				xpos = random.nextInt(34);
				ypos = random.nextInt(21);
			}
			fruitImage.paintIcon(this, g, fruitXpos[xpos], fruitYpos[ypos]);
		}
		
		
		for(int i = 1; i< lengthOfSnake; i++)
		{
			//If its head touches its body part
			if(snakeXlength[i] == snakeXlength[0] && snakeYlength[i] == snakeYlength[0])
			{
				right = false;
				left = false;
				up = false;
				down = false;
//				timer.stop();
				
				//Display the Game Over
				g.setColor(Color.red);
				g.setFont(new Font("areal", Font.BOLD, 40));
				g.drawString("GAME OVER!!! Score:" + score, 250, 300);
				
				//Display Press any Key to continue
				g.setColor(Color.WHITE);
				g.setFont(new Font("areal", Font.BOLD, 20));
				g.drawString("Press ENTER to Restart", 350, 340);
				
			}
		}
		
		
		
		g.dispose();
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		timer.restart();
		
		if(right)
		{
			for(int n = lengthOfSnake-1; n>=0; n--)
			{
				snakeYlength[n+1] = snakeYlength[n];
			}
			
			for(int n = lengthOfSnake; n>=0; n--)
			{
				
				if(n==0)
				{
					snakeXlength[n] = snakeXlength[n] + 25;
				}
				else
				{
					snakeXlength[n] = snakeXlength[n-1];
				}
				//If border crossed
				if(snakeXlength[n] > 850)
				{
					snakeXlength[n] = 25;
				}
			}
			
			repaint();
		}
		
		
		if(left)
		{
			for(int n = lengthOfSnake-1; n>=0; n--)
			{
				snakeYlength[n+1] = snakeYlength[n];
			}
			
			for(int n = lengthOfSnake; n>=0; n--)
			{
				
				if(n==0)
				{
					snakeXlength[n] = snakeXlength[n] - 25;
				}
				else
				{
					snakeXlength[n] = snakeXlength[n-1];
				}
				//If border crossed
				if(snakeXlength[n] < 25)
				{
					snakeXlength[n] = 850;
				}
			}
			
			repaint();
		}
		
		
		if(up)
		{
			for(int n = lengthOfSnake-1; n>=0; n--)
			{
				snakeXlength[n+1] = snakeXlength[n];
			}
			
			for(int n = lengthOfSnake; n>=0; n--)
			{
				
				if(n==0)
				{
					snakeYlength[n] = snakeYlength[n] - 25;
				}
				else
				{
					snakeYlength[n] = snakeYlength[n-1];
				}
				//If border crossed
				if(snakeYlength[n] < 75)
				{
					snakeYlength[n] = 625;
				}
			}
			
			repaint();
		}
		
		
		if(down)
		{
			for(int n = lengthOfSnake-1; n>=0; n--)
			{
				snakeXlength[n+1] = snakeXlength[n];
			}
			
			for(int n = lengthOfSnake; n>=0; n--)
			{
				
				if(n==0)
				{
					snakeYlength[n] = snakeYlength[n] + 25;
				}
				else
				{
					snakeYlength[n] = snakeYlength[n-1];
				}
				//If border crossed
				if(snakeYlength[n] > 625)
				{
					snakeYlength[n] = 75;
				}
			}
			
			repaint();
		}
	}

	@Override
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyPressed(KeyEvent e) {
		
		
		//For Enter Key is Pressed
		if(e.getKeyCode() == KeyEvent.VK_ENTER)
		{
			moves = 0;
			score = 0;
			lengthOfSnake = 3;
			repaint();
		}
		
		//For Right Arrow Press
		if(e.getKeyCode() == KeyEvent.VK_RIGHT)
		{
			moves++;
			right = true;
			
			//if direction if right keep moving towards right
			if(!left)
			{
				right = true;
			}
			//If direction is left,keep moving towards left, and can't go right even by pressing Right Arrow key
			else
			{
				right = false;
				left = true;
			}
			
			up = false;
			down = false;
		}
		
		
		//For Left Arrow Press
		if(e.getKeyCode() == KeyEvent.VK_LEFT)
		{
			moves++;
			left = true;
			
			//if direction if right keep moving towards right
			if(!right)
			{
				left = true;
			}
			//If direction is left,keep moving towards left, and can't go right even by pressing Right Arrow key
			else
			{
				left = false;
				right = true;
			}
			
			up = false;
			down = false;
		}
		
		
		//For Up Arrow Press
		if(e.getKeyCode() == KeyEvent.VK_UP)
		{
			moves++;
			up = true;
			
			//if direction if right keep moving towards right
			if(!down)
			{
				up = true;
			}
			//If direction is left,keep moving towards left, and can't go right even by pressing Right Arrow key
			else
			{
				up = false;
				down = true;
			}
			
			left = false;
			right = false;
		}
		
		
		//For Down Arrow Press
		if(e.getKeyCode() == KeyEvent.VK_DOWN)
		{
			moves++;
			down = true;
			
			//if direction if right keep moving towards right
			if(!up)
			{
				down = true;
			}
			//If direction is left,keep moving towards left, and can't go right even by pressing Right Arrow key
			else
			{
				down = false;
				up = true;
			}
			
			left = false;
			right = false;
		}
		
	}

	@Override
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

}
