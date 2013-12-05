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
      <a class="navbar-brand" href="#">Project name</a>
    </div>
    <div class="navbar-collapse collapse">
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
      <ul class="nav navbar-nav navbar-right">
            <li>{{user}}</li>
            <li><form action="/logout">
          <input class="btn btn-primary" type="submit" value="logout">
      </form></li>
      </ul>
%end
    </div><!--/.navbar-collapse -->
  </div>
</div>

<div class="container">
  <h1>Notes</h1>
  <div class="row">
    <div class="col-md-8">
      <table class="table table-condensed">
        <tr>
          <th>Id</th>
          <th class="col-md-3">Title</th>
          <th class="col-md-5">Note</th>
          <th>Action</th>
        </tr>
        %for row in rows:
        <tr>
          <td>{{row.get('id')}}</td>
          <td>{{row.get('title')}}</td>
          <td>{{row.get('content')}}</td>
          <td><form action="/delete/{{row.get('id')}}">
          %if user is not None:
              <input class="btn btn-danger btn-xs" type="submit" value="Delete Note">
          %else:
              <input class="btn btn-danger btn-xs" type="submit" value="Delete Note" disabled="disabled">
          %end
            </form>
          </td>
        </tr>
        %end
      </table>
    </div>
    <div class="col-md-4">
%if user is not None:
      <div class="panel panel-default">
        <div class="panel-body">
          <form role="form" action="/new" method="POST">
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="title" class="form-control" id="title" placeholder="Enter title" name="title">
            </div>
            <div class="form-group">
              <label for="content">Note:</label>
              <input type="content" class="form-control" id="content" placeholder="Enter note" name="content">
            </div>
            <input class="btn btn-primary" type="submit" value="save" name="save">
          </form>
        </div>
      </div>
%else:
      <h2>Login to add notes</h2>
%end
    </div>
  </div>
</div>
