<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">Notesdude</a>
    </div>
    <div class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li><a href="https://github.com/xorrr/notesdude">Source</a></li>
      </ul>
%if user is None:
      <form class="navbar-form navbar-right" role="form" action="/login" method="POST">
        <div class="form-group">
          <input id="user" type="text" placeholder="User" name="user" class="form-control">
        </div>
        <div class="form-group">
          <input id="password" type="password" placeholder="Password" name="password" class="form-control">
        </div>
        <button type="submit" class="btn btn-success">Sign in</button>
      </form>
%else:
      <form class="navbar-form navbar-right" role="form" action="/logout">
        <button type="submit" class="btn btn-primary" value="logout">Logout</button>
      </form>
%end
    </div><!--/.navbar-collapse -->
  </div>
</div>
