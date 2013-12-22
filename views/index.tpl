% rebase layout
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

<div class="container">
  <div class="row">
    <div class="col-md-8">
      <h1>Notes</h1>
      <table class="table">
        <tr>
          <th class="col-md-3">Title</th>
          <th class="col-md-5">Content</th>
          <th></th>
        </tr>
        %for row in rows:
        <tr>
          <td>{{row.get('title')}}</td>
          <td>{{row.get('content')}}</td>
          <td><form action="/delete/{{row.get('id')}}">
          %if user is not None:
              <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note">
          %else:
              <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note" disabled="disabled">
          %end
            </form>
          </td>
        </tr>
        %end
      </table>
    </div>
  <div class="col-md-4">
%if user is not None and fail is None:
      <div class="panel panel-default">
        <div class="panel-heading">Add Note</div>
        <div class="panel-body">
          <form role="form" action="/new" method="POST">
            <div class="form-group">
              <input type="title" class="form-control" id="title" placeholder="Title" name="title">
            </div>
            <div class="form-group">
              <input type="content" class="form-control" id="content" placeholder="Content" name="content">
            </div>
            <input class="btn btn-success pull-right" type="submit" value="Save Note" name="save">
          </form>
        </div>
      </div>
%elif fail is not None:
      <div class="panel panel-default">
        <div class="panel-heading">Login failed, check your credentials and try again</div>
      </div>
%else:
      <div class="panel panel-default">
        <div class="panel-heading">Sign in to add notes</div>
      </div>
%end
    </div>
  </div>
</div>
